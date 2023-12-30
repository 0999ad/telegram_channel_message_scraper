import time
import requests
from bs4 import BeautifulSoup
import re
import os
import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# Configure logging to write errors to a log file
logging.basicConfig(filename='epochtime.error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')

# Function to extract links from a webpage and save them to a file
def extract_links_and_save(url, output_file):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        response.raise_for_status()

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all links in the webpage
        links = soup.find_all("a")

        # Extract and write the links to the output file
        with open(output_file, "w") as file:
            for link in links:
                href = link.get("href")
                if href and href.startswith("https://t.me/"):
                    file.write(href + "\n")

        print(f"Links have been written to {output_file}")
    except (requests.exceptions.RequestException, Exception) as e:
        error_message = f"Error extracting links: {e}"
        logging.error(error_message)
        print(error_message)

# Function to check if the preview channel contains the keyword
def check_preview_channel(channel_url, keyword):
    try:
        # Initialize a headless Chrome browser
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        # Append "/s/" to the channel URL
        if not channel_url.startswith("https://t.me/s/"):
            channel_url_preview = f"https://t.me/s/{channel_url.split('/')[-1]}"
        else:
            channel_url_preview = channel_url

        # Navigate to the preview URL
        driver.get(channel_url_preview)

        # Wait for a few seconds to ensure the page loads
        time.sleep(5)

        # Get the page source after JavaScript content is generated
        page_source = driver.page_source

        # Parse the page source using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Check if the keyword is present in the preview page (case-insensitive)
        preview_text = soup.get_text()
        keyword_found = re.search(keyword, preview_text, re.IGNORECASE) is not None

        if keyword_found:
            # Find all message text elements
            message_texts = soup.find_all('div', class_='tgme_widget_message_text')
            
            # Extract and return the entire message text when the keyword is found
            for text_element in message_texts:
                message_text = text_element.get_text()
                if re.search(keyword, message_text, re.IGNORECASE):
                    return message_text, channel_url_preview

        return None, channel_url_preview
    except (WebDriverException, Exception) as e:
        error_message = f"Error checking preview channel: {e}"
        logging.error(error_message)
        print(error_message)
        return None, channel_url

    finally:
        # Close the browser
        driver.quit()

# Function to create a new links file with the current epoch time in the filename
def create_links_file():
    try:
        # URL of the GitHub Markdown file
        github_url = "https://github.com/fastfire/deepdarkCTI/blob/main/telegram.md"

        # Initialize a headless Chrome browser
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        # Navigate to the GitHub URL
        driver.get(github_url)

        # Wait for a few seconds to ensure the page loads and JavaScript content is generated
        time.sleep(5)

        # Get the page source after JavaScript content is generated
        page_source = driver.page_source

        # Parse the page source using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all links in the HTML content
        links = soup.find_all("a", href=True)

        # Filter links that start with "https://t.me/"
        filtered_links = [link["href"] for link in links if link["href"].startswith("https://t.me/")]

        # Create a new links file with the current epoch time in the filename
        epoch_time = int(time.time())
        links_filename = f"{epoch_time}.links.txt"

        # Write the filtered links to the new links file
        with open(links_filename, "w") as file:
            for link in filtered_links:
                if not link.startswith("https://t.me/s/"):
                    link = f"https://t.me/s/{link.split('/')[-1]}"
                file.write(link + "\n")

        print(f"Found {len(filtered_links)} links starting with 'https://t.me/' and saved them to '{links_filename}'")
        return links_filename
    except (WebDriverException, Exception) as e:
        error_message = f"Error creating links file: {e}"
        logging.error(error_message)
        print(error_message)
        return None
    finally:
        # Close the browser
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
    # Create a new links file or use the latest one
    links_filename = create_links_file()
    if not links_filename:
        return

    # Wait for 10 seconds
    time.sleep(10)

    # Read the channel URLs from the links file and scrape each channel
    with open(links_filename, "r") as file:
        channel_urls = file.read().splitlines()
        # User input: Keyword to search for
        keyword = input("Enter the keyword to search for: ")

        # Create a results filename with the current epoch time in the filename
        epoch_time = int(time.time())
        results_filename = f"{epoch_time}.results.txt"

        for channel_url in channel_urls:
            print(f"Checking preview for {channel_url}")
            message_text, updated_channel_url = check_preview_channel(channel_url, keyword)
            if message_text:
                write_results_to_file(results_filename, message_text)
                print(f"Keyword found in {updated_channel_url} (Written to {results_filename})")
            else:
                print("Preview not available or keyword not found, skipping...")

    print("Scraping and keyword search completed.")

if __name__ == "__main__":
    main()
