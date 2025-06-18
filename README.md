# Laravel Documentation Scraper

> A Python scraper that downloads and converts the official Laravel documentation into clean, LLM-friendly Markdown files.

## The Problem

Large Language Models (LLMs) like ChatGPT and Gemini are fantastic aids for development. However, their knowledge is based on a snapshot of data from the past, which can be outdated for rapidly evolving frameworks like Laravel. This often leads to them suggesting deprecated functions, outdated syntax, or being unaware of new features.

## The Solution

This scraper bridges the knowledge gap. It fetches the official Laravel documentation directly from the source for any given version. It then intelligently converts each page into a clean Markdown file, with a special focus on preserving code block formatting.

The resulting `.md` files can be fed directly into an LLM's context window. This provides the AI with up-to-date, accurate information, enabling it to generate relevant and correct code and answers for your Laravel projects.

## Features

- **Fetches All Versions**: Automatically gets a list of all available documentation versions from `laravel.com`.
- **Interactive UI**: Prompts the user with a clean, interactive list to select the desired version to scrape.
- **Structured Output**: Saves the generated Markdown files into a version-specific directory (e.g., `docs/12.x/`) for easy organization.
- **Intelligent Conversion**: Uses `html2text` to convert the main content into Markdown.
- **LLM-Friendly Code Blocks**: Correctly identifies code blocks and their language (`php`, `shell`, etc.) and formats them using proper Markdown fences, which is critical for AI understanding.
- **Rich Console Output**: Provides an informative console experience with progress bars and status updates using `rich`.

## Installation

Follow these steps to set up the project locally. Using a virtual environment is strongly recommended to avoid conflicts with system-wide packages.

1.  **Clone the repository:**
    ```shell
    git clone https://github.com/devcedme/laravel-docs-scraper.git
    cd laravel-docs-scraper
    ```

2.  **Set up a virtual environment:**
    * First, ensure you have the `venv` module. On Debian/Ubuntu, you might need to install it:
        ```shell
        sudo apt update && sudo apt install python3-venv
        ```
    * Create the virtual environment:
        ```shell
        python3 -m venv venv
        ```
    * Activate it:
        ```shell
        source venv/bin/activate
        ```
        *(On Windows, use `.\venv\Scripts\activate`)*

3.  **Install the required dependencies:**
    With your virtual environment active, install the necessary packages.
    ```shell
    pip install -r requirements.txt
    ```

## Usage

Simply run the main script from your terminal. Make sure your virtual environment is active first.
```shell
python main.py
```
You will be presented with an interactive prompt to select the Laravel version you wish to download. The script will then create the necessary directories and begin scraping.

To leave the virtual environment when you are done, simply type:
```shell
deactivate
```

## Dependencies
- **requests**: For making HTTP requests to fetch the documentation pages.
- **beautifulsoup4**: For parsing the HTML content.
- **html2text**: For converting the cleaned HTML into Markdown.
- **questionary**: To create the user-friendly interactive version selection prompt.
- **rich**:  To display beautiful formatting, progress bars, and logs in the console.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full license rights and limitations.

## Contributing

Contributions are welcome! If you have ideas for improvements or find a bug, please open an issue or submit a pull request.
