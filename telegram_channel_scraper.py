import time
import requests
from bs4 import BeautifulSoup
import re
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
    """
    Prints a header for the script.
    """
    print("****************************************")
    print("* TGS TELE-SCRAPER                     *")
    print("*                                      *")
    print("* For educational purposes only.       *")
    print("* Use responsibly and legally.         *")
    print("****************************************")

def get_current_datetime_formatted():
    """
    Returns the current date and time in a specified format.
    """
    return datetime.datetime.now().strftime("%y-%m-%d-%H%M%S")

def extract_links_and_save(url, output_file):
    """
    Extracts links from a webpage and saves them to a file.

    Args:
    url (str): The URL to scrape.
    output_file (str): The name of the file to save the links.
    """
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
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as e:
        logging.error(f"Error extracting links: {e}")

def check_search_results(search_url, keyword):
    """
    Checks the search results page for a single keyword and returns matching results.

    Args:
    search_url (str): URL to search.
    keyword (str): Keyword to search for.

    Returns:
    str: A formatted string containing search results.
    """
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        # Handling pagination
        while True:
            result_elements = soup.find_all('div', class_='search-result')
            for result_element in result_elements:
                result_text = result_element.get_text()
                if re.search(keyword, result_text, re.IGNORECASE):
                    results.append(result_text)

            next_page = soup.find('a', text='Next')
            if next_page:
                response = requests.get(next_page['href'])
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
            else:
                break

        return "\n".join(results)
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return ""
    except Exception as e:
        logging.error(f"Error checking search results: {e}")
        return ""

def create_links_file():
    """
    Creates a new links file by scraping a specific GitHub page.

    Returns:
    str: The filename of the created links file, or None if an error occurred.
    """
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
    except WebDriverException as web_driver_err:
        logging.error(f"WebDriver error: {web_driver_err}")
        return None
    except Exception as e:
        logging.error(f"Error creating links file: {e}")
        return None
    finally:
        driver.quit()

def write_results_to_file(results_filename, message_text):
    """
    Writes results to a file.

    Args:
    results_filename (str): The name of the file to write the results to.
    message_text (str): The text to write to the file.
    """
    try:
        with open(results_filename, "a", encoding='utf-8') as file:
            file.write(message_text + "\n")
    except Exception as e:
        logging.error(f"Error writing results to file: {e}")

def add_to_crontab(keywords, script_path):
    """
    Adds a job to the crontab to run this script periodically.

    Args:
    keywords (list): A list of keywords for the script to search for.
    script_path (str): The path to the script.
    """
    job_command = f"0 */6 * * * /usr/bin/python3 {script_path} {' '.join(keywords)}"
    try:
        subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE, check=True)
        subprocess.run(['(crontab -l; echo "{}") | crontab -'.format(job_command)], shell=True, check=True)
        print("Added to crontab to run every 6 hours.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Crontab error: {e}")
        print("No existing crontab found. Creating a new one.")
        subprocess.run(['echo "{}" | crontab -'.format(job_command)], shell=True, check=True)

def main():
    """
    Main function to orchestrate the web scraping and searching tasks.
    """
    print_header()

    start_time = get_current_datetime_formatted()
    print(f"Script started at: {start_time}")

    links_filename = create_links_file()
    if not links_filename:
        return

    time.sleep(10)

    if len(sys.argv) > 1:
        keywords = sys.argv[1:]
    else:
        keywords_input = ''
        while not keywords_input:
            keywords_input = input("Enter keywords to search for (comma-separated): ").strip()
            if not keywords_input:
                print("You must enter at least one keyword.")
        keywords = [keyword.strip() for keyword in keywords_input.split(',')]

        add_to_cron = input("Do you want to add this task to crontab to run every 6 hours? (Y/N): ").strip().upper()
        if add_to_cron == 'Y':
            script_path = input("Enter the full path to the script: ").strip()
            add_to_crontab(keywords, script_path)

    current_datetime = get_current_datetime_formatted()
    results_filename = f"{current_datetime}-results.txt"

    with open(links_filename, "r") as file:
        channel_urls = file.read().splitlines()

        for channel_url in channel_urls:
            for keyword in keywords:
                print(f"Checking search results for {channel_url} (Keyword: {keyword})")
                search_url = f"{channel_url}?q={keyword}"
                message_text = check_search_results(search_url, keyword)
                if message_text:
                    write_results_to_file(results_filename, message_text)
                    print(f"{keyword} found in {channel_url} (Written to {results_filename})")
                else:
                    print(f"{keyword} not found in {channel_url}, skipping...")

    end_time = get_current_datetime_formatted()
    print(f"Script finished at: {end_time}")
    print("Scraping and keyword search completed.")

if __name__ == "__main__":
    main()
