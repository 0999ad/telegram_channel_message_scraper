import time
import requests
from bs4 import BeautifulSoup
import re
import os
import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import datetime
import subprocess
import sys

# Configure logging to write errors to a log file
logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s: %(message)s")

def print_header():
    print("****************************************")
    print("* TGS TELE-SCRAPER                     *")
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

        results = []
        if matching_keywords:
            message_texts = soup.find_all('div', class_='tgme_widget_message_text')
            for text_element in message_texts:
                message_text = text_element.get_text()
                for keyword in matching_keywords:
                    if re.search(keyword, message_text, re.IGNORECASE):
                        results.append(f"______\n{keyword} Found\n{channel_url_preview} Match\n{message_text}\n--------\nNext message\n")
            return "\n".join(results)
        return ""
    except (WebDriverException, Exception) as e:
        error_message = f"Error checking preview channel: {e}"
        logging.error(error_message)
        print(error_message)
        return ""
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

def add_to_crontab(keywords, script_path):
    # Crontab command to run the script every 6 hours with the specified keywords
    job_command = f"0 */6 * * * /usr/bin/python3 {script_path} {' '.join(keywords)}"
    try:
        subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, check=True)
        subprocess.run(['(crontab -l; echo "{}") | crontab -'.format(job_command)], shell=True, check=True)
        print("Added to crontab to run every 6 hours.")
    except subprocess.CalledProcessError:
        print("No existing crontab found. Creating a new one.")
        subprocess.run(['echo "{}" | crontab -'.format(job_command)], shell=True, check=True)

# Main function
def main():
    print_header()

    start_time = get_current_datetime_formatted()
    print(f"Script started at: {start_time}")

    links_filename = create_links_file()
    if not links_filename:
        return

    time.sleep(10)

    if len(sys.argv) > 1:
        # Use command-line arguments if provided
        keywords = sys.argv[1:]
    else:
        # Prompt for keywords if not running from crontab
        keywords_input = ''
        while not keywords_input:
            keywords_input = input("Enter keywords to search for (comma-separated): ").strip()
            if not keywords_input:
                print("You must enter at least one keyword.")
        keywords = [keyword.strip() for keyword in keywords_input.split(',')]

        # Ask user if they want to add to crontab
        add_to_cron = input("Do you want to add this task to crontab to run every 6 hours? (Y/N): ").strip().upper()
        if add_to_cron == 'Y':
            script_path = input("Enter the full path to the script: ").strip()
            add_to_crontab(keywords, script_path)

    current_datetime = get_current_datetime_formatted()
    results_filename = f"{current_datetime}-results.txt"

    with open(links_filename, "r") as file:
        channel_urls = file.read().splitlines()

        for channel_url in channel_urls:
            print(f"Checking preview for {channel_url}")
            message_text = check_preview_channel(channel_url, keywords)
            if message_text:
                write_results_to_file(results_filename, message_text)
                print(f"Keyword(s) found in {channel_url} (Written to {results_filename})")
            else:
                print("Preview not available or keyword(s) not found, skipping...")

    end_time = get_current_datetime_formatted()
    print(f"Script finished at: {end_time}")
    print("Scraping and keyword search completed.")

if __name__ == "__main__":
    main()
