# GPT GitHub Crawler
A tool that crawls GitHub repositories instead of sites. Enabling users to crawl repository trees, match file patterns, and decode file contents. This tool is ideal for extracting and processing data from these repositories to upload to your custom GPT.

## Features
- **Recursive GitHub Repository Crawling:** Efficiently traverses the GitHub repository tree.
- **Pattern Matching:** Utilizes patterns to selectively crawl files in the repository.
- **Content Decoding:** Automatically decodes file contents for easy processing.
- **Configurable via JSON:** Allows easy configuration through an external `config.json` file.
- **JSON Output:** Outputs the crawled data into a structured JSON file.

## Prerequisites
Before starting, ensure you have the following:
- Python 3.6 or higher.
- GitHub personal access token.

## Installation
First, clone the repository:

```bash
git clone https://github.com/your-username/gpt-github-crawler.git
```

Then, navigate to the cloned directory:

```bash
cd gpt-github-crawler
```

### Setting Up the Environment
Install the required environment using Conda:

```bash
conda env create -f environment.yml
```

Activate the environment:

```bash
conda activate gpt-github-crawler
```

### Installing the Package
After activating the Conda environment, install the package in editable mode:

```bash
pip install -e .
```

This command installs the package and makes it available as a command-line tool. It also ensures that any changes you make to the code are immediately reflected when you run the tool.

## Configuration
The crawler script uses a configuration file named `config.json` by default, located in the same directory as the script. Create your configuration file with the following format:

```json
{
    "repo_owner": "<repository_owner>",
    "repo_name": "<repository_name>",
    "branch_name": "<branch_name>",
    "match": ["<pattern_to_match_files>",...],
    "ignore": ["<pattern_to_ignore_files>",...],
    "max_files_to_crawl": <max_number_of_files>,
    "output_file_name": "<output_filename>.json",
    "github_token": "<your_github_token>"
}
```

Fill in the placeholders with your GitHub repository details and personal access token. Leave ignore as an empty list if you don't want to ignore any patterns. The output_file_name accepts both absolute and relative paths. If a relative path is provided, it will be resolve relative to the directory where the script is located.

## Run your crawler
Once the package is installed and configuration file is created, you can run the script from anywhere in your system using the command:

```bash
gpt-github-crawler
```

This command will execute the crawler script according to the configuration specified in `config.json`.

You can specify a different configuration file using the `--config` argument when running the script. This argument is optional, and accepts both absolute and relative paths. If a relative path is provided, it will be resolved relative to the directory where the script is located.

For example, to use a configuration file located at `/path/to/your/config.json`, you can run the script like this:

```bash
gpt-github-crawler --config /path/to/your/config.json
```

These commands will generate a JSON file with the results to the output_file_name path that is specified.

## Contributing
Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Create a new Pull Request.

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements
This project is inspired by and based on concepts from the [BuilderIO/gpt-crawler](https://github.com/BuilderIO/gpt-crawler).
