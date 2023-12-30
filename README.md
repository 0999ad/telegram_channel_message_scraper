# Telegram Channel Scraper

## Overview

The Telegram Channel Scraper is a Python script designed to extract links from a specified webpage, check for keyword matches in the preview of Telegram channels linked on the page, and save the results to a file. This script can be particularly useful for researchers and analysts who want to monitor Telegram channels for specific topics or keywords.

## Features

- Extracts links from a specified webpage.
- Checks Telegram channel previews for specified keywords.
- Saves matching messages from Telegram channels to a results file.
- Handles errors gracefully and logs them to an error log file.

## Requirements

- Python 3.x
- Selenium WebDriver (ChromeDriver)
- Chrome browser
- BeautifulSoup4
- Requests library

## Installation

1. Install Python 3.x from the [official Python website](https://www.python.org/downloads/).

2. Install the required Python libraries using pip:

   ```
   pip install selenium beautifulsoup4 requests
   ```

3. Download the ChromeDriver WebDriver for your specific Chrome version from the [official ChromeDriver website](https://sites.google.com/chromium.org/driver/). Make sure to place the ChromeDriver executable in a directory that's included in your system's PATH.

## Usage

1. Clone or download the script from the GitHub repository:

   ```
   git clone https://github.com/yourusername/telegram-channel-scraper.git
   ```

2. Navigate to the script's directory:

   ```
   cd telegram-channel-scraper
   ```

3. Run the script:

   ```
   python telegram_channel_scraper.py
   ```

4. Follow the on-screen instructions to provide the URL of the webpage to scrape, the keyword to search for, and to monitor the progress.

## Configuration

- You can configure the script's behavior by modifying the options in the `telegram_channel_scraper.py` file, such as specifying the sleep duration, error log filename, and more.

## Error Handling

- The script handles potential errors gracefully, including HTTP request errors, WebDriver exceptions, and file I/O errors. Error details are logged in the `epochtime.error.log` file.

## License

This script is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The script was inspired by the need to monitor Telegram channels for specific keywords.

---
