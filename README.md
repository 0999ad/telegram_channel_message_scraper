# README for Web Scraping and Keyword Search Script
## Legal Disclaimer

### Educational Use and Compliance with Local Laws
This script is provided for educational purposes only. Users are responsible for ensuring that their use of the script complies with local legal laws and regulations. The originator of this code disclaims any responsibility for unethical or illegal use of the script. Users should exercise due diligence and respect the terms of service and data usage policies of the websites they interact with using this script.

## Overview
This Python script is designed for scraping web pages, specifically targeting Telegram channel links from a specified GitHub page, and then searching for user-defined keywords within these channels. It utilizes libraries such as `requests`, `BeautifulSoup`, and `selenium` for web scraping, and `re` for regular expression operations. The script is structured to handle errors gracefully and logs them for troubleshooting.

## Features
- **Link Extraction**: Extracts Telegram channel links from a specified GitHub page.
- **Keyword Search**: Searches for user-defined keywords within the preview text of Telegram channels.
- **File Management**: Saves extracted links and search results to timestamped files for easy tracking.
- **Error Logging**: Logs errors to a file, aiding in debugging and maintenance.

## Requirements
- Python 3.x
- Libraries: `requests`, `bs4` (BeautifulSoup), `selenium`, `re`, `datetime`, `logging`
- Selenium WebDriver (e.g., ChromeDriver)

## Installation
1. Ensure Python 3.x is installed on your system.
2. Install required Python libraries:
   ```
   pip install requests beautifulsoup4 selenium
   ```
3. Install Chrome Webdriver (Selenium):
   Since the script uses Selenium for web scraping, you need to download the Chrome WebDriver and make sure it's available in your system's PATH.
   You can download the Chrome WebDriver from the following link: https://sites.google.com/chromium.org/driver/
   After downloading, unzip the WebDriver executable and place it in a directory that is included in your system's PATH environment variable.
   Alternatively, you can specify the WebDriver path in the script if you don't want to place it in the PATH.

## Usage
1. Run the script using Python:
   ```
   python script_name.py
   ```
2. Enter the keywords when prompted. Keywords should be comma-separated.
3. The script will process the data and output results to timestamped files.

## Functions
- `get_current_datetime_formatted()`: Returns the current date and time in a specific format for file naming.
- `extract_links_and_save(url, output_file)`: Extracts links from the specified URL and saves them to a file.
- `check_preview_channel(channel_url, keywords)`: Checks if the preview of a Telegram channel contains any of the provided keywords.
- `create_links_file()`: Creates a new file with extracted Telegram channel links.
- `write_results_to_file(results_filename, message_text)`: Writes the search results to a file, separating entries with asterisks.
- `main()`: The main function orchestrating the script's workflow.

## Output Files
- **Links File**: Contains the extracted Telegram channel links.
- **Results File**: Contains the search results with each entry separated by asterisks.

## Error Handling
Errors are logged to `error.log`, which includes timestamps and error messages for troubleshooting.

## Note
This script is intended for educational purposes and should be used in accordance with web scraping and data usage policies of the respective websites.

---

Replace `script_name.py` with the actual name of your Python script file. This README provides a comprehensive guide for users to understand, install, and use your script effectively.
