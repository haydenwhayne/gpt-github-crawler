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
Create your `config.json` in the project root, which has the following format:

```json
{
    "repo_owner": "<repository_owner>",
    "repo_name": "<repository_name>",
    "branch_name": "<branch_name>",
    "match": ["<pattern_to_match_files>",...],
    "max_files_to_crawl": <max_number_of_files>,
    "output_file_name": "<output_filename>.json",
    "github_token": "<your_github_token>"
}
```

Fill in the placeholders with your GitHub repository details and personal access token.

## Run your crawler
Once the package is installed, you can run the script from anywhere in your system using the command:

```bash
gpt-github-crawler
```

This command will execute the crawler script according to the configuration specified in `config.json` and generate a JSON file with the results.

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
