import time
import requests
from bs4 import BeautifulSoup
import re
import os
import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import datetime

# Configure logging to write errors to a log file
logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s: %(message)s')

def print_header():
    print("****************************************")
    print("* LFA TELE-SCRAPER                     *")
    print("* https://github.com/0999ad/           *")
    print("*                                      *")
    print("* For educational purposes only.       *")
    print("* Use responsibly and legally.         *")
    print("****************************************")

# Function to get the current date and time in the specified format
def get_current_datetime_formatted():
    return datetime.datetime.now().strftime("%y-%m-%d-%H%M%S")

# Function to extract links from a webpage and save them to a file
def extract_links_and_save(url, output_file):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")

        current_datetime = get_current_datetime_formatted()
        formatted_output_file = f"{current_datetime}-{output_file}"

        with open(formatted_output_file, "w") as file:
            for link in links:
                href = link.get("href")
                if href and href.startswith("https://t.me/"):
                    file.write(href + "\n")

        print(f"Links have been written to {formatted_output_file}")
    except (requests.exceptions.RequestException, Exception) as e:
        error_message = f"Error extracting links: {e}"
        logging.error(error_message)
        print(error_message)

# Function to check if the preview channel contains any of the provided keywords
def check_preview_channel(channel_url, keywords):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        if not channel_url.startswith("https://t.me/s/"):
            channel_url_preview = f"https://t.me/s/{channel_url.split('/')[-1]}"
        else:
            channel_url_preview = channel_url

        driver.get(channel_url_preview)
        time.sleep(5)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        preview_text = soup.get_text()
        matching_keywords = [keyword for keyword in keywords if re.search(keyword, preview_text, re.IGNORECASE)]

        if matching_keywords:
            message_texts = soup.find_all('div', class_='tgme_widget_message_text')
            for text_element in message_texts:
                message_text = text_element.get_text()
                for keyword in matching_keywords:
                    if re.search(keyword, message_text, re.IGNORECASE):
                        return message_text, channel_url_preview

        return None, channel_url_preview
    except (WebDriverException, Exception) as e:
        error_message = f"Error checking preview channel: {e}"
        logging.error(error_message)
        print(error_message)
        return None, channel_url
    finally:
        driver.quit()

# Function to create a new links file
def create_links_file():
    try:
        github_url = "https://github.com/fastfire/deepdarkCTI/blob/main/telegram.md"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        driver.get(github_url)
        time.sleep(5)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        links = soup.find_all("a", href=True)
        filtered_links = [link["href"] for link in links if link["href"].startswith("https://t.me/")]

        current_datetime = get_current_datetime_formatted()
        links_filename = f"{current_datetime}-links.txt"

        with open(links_filename, "w") as file:
            for link in filtered_links:
                if not link.startswith("https://t.me/s/"):
                    link = f"https://t.me/s/{link.split('/')[-1]}"
                file.write(link + "\n")

        print(f"Found {len(filtered_links)} links and saved them to '{links_filename}'")
        return links_filename
    except (WebDriverException, Exception) as e:
        error_message = f"Error creating links file: {e}"
        logging.error(error_message)
        print(error_message)
        return None
    finally:
        driver.quit()

# Function to write results to a file
def write_results_to_file(results_filename, message_text):
    try:
        with open(results_filename, "a", encoding='utf-8') as file:
            file.write(message_text + "\n")
    except Exception as e:
        error_message = f"Error writing results to file: {e}"
        logging.error(error_message)
        print(error_message)

# Main function
def main():
    print_header()

    start_time = get_current_datetime_formatted()
    print(f"Script started at: {start_time}")

    links_filename = create_links_file()
    if not links_filename:
        return

    time.sleep(10)

    with open(links_filename, "r") as file:
        channel_urls = file.read().splitlines()

        keywords_input = input("Enter keywords to search for (comma-separated): ")
        keywords = [keyword.strip() for keyword in keywords_input.split(',')]

        current_datetime = get_current_datetime_formatted()
        results_filename = f"{current_datetime}-results.txt"

        for channel_url in channel_urls:
            print(f"Checking preview for {channel_url}")
            message_text, updated_channel_url = check_preview_channel(channel_url, keywords)
            if message_text:
                write_results_to_file(results_filename, message_text)
                print(f"Keyword(s) found in {updated_channel_url} (Written to {results_filename})")
            else:
                print("Preview not available or keyword(s) not found, skipping...")

    end_time = get_current_datetime_formatted()
    print(f"Script finished at: {end_time}")
    print("Scraping and keyword search completed.")

if __name__ == "__main__":
    main()
