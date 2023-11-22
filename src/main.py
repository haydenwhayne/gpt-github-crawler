import requests
import base64
import fnmatch
import json
import logging
import os
    
def main():
    setup_logging()
    logging.info("Starting the crawler...")

    # Get the absolute path of the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path of the config.json file
    config_file_path = os.path.join(current_dir, '..', 'config.json')

    # Check if the config.json file exists
    if not os.path.exists(config_file_path):
        raise FileNotFoundError("The config.json file does not exist. Make sure you have created it in the root directory.")

    # Load configuration from the config.json file
    with open(config_file_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)

    # Check config
    check_config(config)

    # Run the crawler
    crawled_data = crawl_github_repo(config)

    total = len(crawled_data)
    successful = len([item for item in crawled_data if item['content']])
    failed = total - successful

    # Save the crawled data to a file
    save_to_file(crawled_data, config['output_file_name'])

    logging.info(f"Finished! Total {total} request: {successful} successful, {failed} failed.")
    
def setup_logging():
    # Configure the logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_config(config: dict):
    if 'match' not in config or not isinstance(config['match'], list):
        raise ValueError("The config file must contain a list of match patterns.")
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
    if 'output_file_name' not in config or not isinstance(config['output_file_name'], str):
        raise ValueError("The config file must contain a string of output file name.")

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

def get_file_content(file_url: str, github_token: str):
    print(f"Crawling {file_url}")
    
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(file_url, headers=headers)
    if response.status_code == 200:
        content = response.json().get('content', '')
        decoded_content = base64.b64decode(content).decode('utf-8')
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
                if count >= config['max_files_to_crawl']:
                    break
                file_content = get_file_content(item['url'], config['github_token'])
                file_url = f"https://github.com/{config['repo_owner']}/{config['repo_name']}/blob/{config['branch_name']}/{item['path']}"
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
