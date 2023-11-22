import requests
import base64
import fnmatch
import json
import logging
import os
import argparse
    
def main():
    parser = argparse.ArgumentParser(description="A simple web crawler")
    parser.add_argument("--config", help="Path to the configuration file")
    args = parser.parse_args()
    
    setup_logging()
    logging.info("Starting the crawler...")

    # Get the absolute path of the current directory
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # If --config argument is provided and it's not an absolute path, join it with current_dir
    # If it's an absolute path, use it as is
    # If --config argument is not provided, use 'config.json' in the current directory
    if args.config:
        config_file_path = os.path.join(current_dir, args.config) if not os.path.isabs(args.config) else args.config
    else:
        config_file_path = os.path.join(current_dir, 'config.json')

    # Check if the config file ends with .json
    if not config_file_path.endswith('.json'):
        raise ValueError("The config file must be a JSON file.")
    
    # Check if the config.json file exists
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"The {config_file_path} file does not exist.")

    # Load configuration from the config.json file
    with open(config_file_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)

    # Check config
    check_config(config)

    # If the output_file_name in the config.json is not an absolute path, join it with current_dir
    output_file_path = os.path.join(current_dir, config['output_file_name']) if not os.path.isabs(config['output_file_name']) else config['output_file_name']

    # Check if the output file directory exists
    if not os.path.exists(os.path.dirname(output_file_path)):
        raise FileNotFoundError(f"The {os.path.dirname(output_file_path)} directory does not exist.")

    # Run the crawler
    crawled_data = crawl_github_repo(config)

    total = len(crawled_data)
    successful = len([item for item in crawled_data if item['content']])
    failed = total - successful

    # Save the crawled data to a file
    save_to_file(crawled_data, output_file_path)

    logging.info(f"Finished! Total {total} request: {successful} successful, {failed} failed.")
    
def setup_logging():
    # Configure the logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_config(config: dict):
    if 'match' not in config or not isinstance(config['match'], list):
        raise ValueError("The config file must contain a list of match patterns.")
    if 'ignore' not in config or not isinstance(config['ignore'], list):
        raise ValueError("The config file must contain a list of ignore patterns.")
    if 'repo_owner' not in config or not isinstance(config['repo_owner'], str):
        raise ValueError("The config file must contain a string of repo owner.")
    if 'repo_name' not in config or not isinstance(config['repo_name'], str):
        raise ValueError("The config file must contain a string of repo name.")
    if 'branch_name' not in config or not isinstance(config['branch_name'], str):
        raise ValueError("The config file must contain a string of branch name.")
    if 'github_token' not in config or not isinstance(config['github_token'], str):
        raise ValueError("The config file must contain a string of your github personal access token.")
    if 'max_files_to_crawl' not in config or not (isinstance(config['max_files_to_crawl'], int) or isinstance(config['max_files_to_crawl'], float)):
        raise ValueError("The config file must contain an integer or float of max files to crawl.")
    if 'output_file_name' not in config or not isinstance(config['output_file_name'], str) or not config['output_file_name'].endswith('.json'):
        raise ValueError("The config file must contain a string of output file name and it must be a JSON file.")

def check_github_status_code(response: requests.Response):
    # Check the status code of the response and print the json message if it exists
    status_code = response.status_code
    message = response.json().get('message', '')
    if status_code == 401:
        logging.error(f"401 Unauthorized. {message}. Please check your github personal access token and make sure it is valid.")
    elif status_code == 403:
        logging.error(f"403 Forbidden: {message}. Please check your github personal access token and make sure it has the right permissions (e.g. Read-Only Contents and Metadata).")
    elif status_code == 404:
        logging.error(f"404 Not Found: {message}. Please check your repo owner, repo name and branch name. If accessing a private repo, make sure your github personal access token has the right permissions (e.g. Read-Only Contents and Metadata).")
    elif status_code == 429:
        logging.error(f"429 Too Many Requests: {message}. Try again later.")
    elif status_code == 500:
        logging.error(f"500 Internal Server Error: {message}. Try again later.")
    else:
        logging.error(f"Status Code {status_code}: {message}. Please check your config file and try again.")

def format_ipynb_content(decoded_content):
    content_dict = json.loads(decoded_content)
    formatted_content = []
    
    cells = content_dict.get('cells', [])  # For .ipynb version 4 and above
    if not cells:
        # For .ipynb version 3 and below
        worksheets = content_dict.get('worksheets', [])
        cells = [cell for worksheet in worksheets for cell in worksheet.get('cells', [])]
    
    for cell in cells:
        if cell['cell_type'] in ['code', 'markdown']:
            source = cell.get('source', [])
            cell_content = ''.join(source)
            formatted_content.append(f"--- cell type: {cell['cell_type']} ---\n{cell_content}")
    
    return '\n'.join(formatted_content)

def get_file_content(url: str, file_url: str, github_token: str):
    print(f"Crawling {file_url}")
    
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json().get('content', '')
        decoded_content = base64.b64decode(content).decode('utf-8')
        if file_url.endswith('.ipynb'):
            return format_ipynb_content(decoded_content)
        return decoded_content
    else:
        check_github_status_code(response)
        return None

def crawl_github_repo(config: dict):
    api_url = f"https://api.github.com/repos/{config['repo_owner']}/{config['repo_name']}/git/trees/{config['branch_name']}?recursive=1"
    headers = {'Authorization': f'token {config["github_token"]}'}
    response = requests.get(api_url, headers=headers)
    crawled_files = []

    if response.status_code == 200:
        tree = response.json().get('tree', [])
        count = 0

        for item in tree:
            if item['type'] == 'blob' and any(fnmatch.fnmatch(item['path'], pattern) for pattern in config['match']):
                if any(fnmatch.fnmatch(item['path'], pattern) for pattern in config['ignore']):
                    continue  # Ignore the file if it matches any ignore pattern
                if count >= config['max_files_to_crawl']:
                    break
                file_url = f"https://github.com/{config['repo_owner']}/{config['repo_name']}/blob/{config['branch_name']}/{item['path']}"
                file_content = get_file_content(item['url'], file_url, config['github_token'])
                if file_content:
                    crawled_files.append({'url': file_url, 'content': file_content})
                else:
                    crawled_files.append({'url': file_url, 'content': ''})
                count += 1
    else:
        check_github_status_code(response)

    return crawled_files

def save_to_file(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
