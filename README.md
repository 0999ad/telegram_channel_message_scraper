# README for TGS TELE-SCRAPER
This has been run on a MacBook Pro macOS Ventura Version 13.6 (22G120)
## Introduction

The TGS TELE-SCRAPER is a Python script designed for educational and research purposes, facilitating the automated extraction of specific content from Telegram channels. The script scrapes Telegram channel URLs from a predefined source, then searches these channels for user-defined keywords, and logs the results. It's built with the intent to be used responsibly and legally, adhering to the terms of service of the sources it interacts with.

## Features

- **Automated Link Extraction**: Extracts Telegram channel URLs from a specified webpage.
- **Keyword Searching**: Searches through the content of these channels for user-defined keywords.
- **Cron Job Integration**: Option to add the script to crontab for periodic execution every 6 hours.
- **Results Logging**: Logs the findings in a structured format for easy review.

## How It Works

The script operates in several steps:

1. **Link Extraction**: 
   - It first connects to a specified webpage (currently hardcoded as a GitHub page) and extracts all Telegram channel URLs listed there.
   - These URLs are saved to a timestamped file for further processing.

2. **Content Scrapping**:
   - The script then iterates over each extracted Telegram channel URL.
   - It uses Selenium with a headless Chrome browser to render the content of the channel.
   - The content is parsed using BeautifulSoup to extract text.

3. **Keyword Search**:
   - Users are prompted to input keywords, which the script will search for in the content of each Telegram channel.
   - If a keyword is found, the script logs the keyword, the URL of the channel, and the matched message text.

4. **Cron Job Integration** (Optional):
   - Users have the option to schedule the script to run automatically every 6 hours.
   - If chosen, the script's execution command along with the schedule is added to the user's crontab.

5. **Results Logging**:
   - The results are logged in a file with a clear format, showing each found keyword, the corresponding Telegram channel URL, and the message text where the keyword was found.

## Setup and Usage

### Prerequisites

- Python 3.x
- Selenium WebDriver
- Chrome Browser and corresponding ChromeDriver
- BeautifulSoup4
- Requests

### Installation

1. Clone the repository or download the script to your local machine.
2. Install the required Python packages: `selenium`, `beautifulsoup4`, `requests`.

   ```bash
   pip install selenium beautifulsoup4 requests
   ```

3. Ensure you have Chrome and ChromeDriver installed that matches your Chrome version.

### Running the Script

1. Navigate to the script's directory in your terminal.
2. Run the script using Python.

   ```bash
   python extract_search.py
   ```

3. Follow the on-screen prompts to enter keywords or set up a cron job.

### Adding to Crontab

- If you opt to add the script to crontab, you will be prompted for the full path of the script and the keywords to search. The script will then be scheduled to run every 6 hours automatically.

## License

This script is provided for educational purposes only. Users are responsible for ensuring they adhere to all applicable laws and terms of service when using this script.

---

*Note: The above README is a template and should be adjusted based on the specific implementation details of the TGS TELE-SCRAPER script.*
