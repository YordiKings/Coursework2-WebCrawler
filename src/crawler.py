import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

BASE_URL = "https://quotes.toscrape.com"
POLITENESS_DELAY = 6

def crawl():
    visited_urls = set()
    pages_data = {}
    url_queue = ["/"]

    while url_queue:
        current_path = url_queue.pop(0)
        full_url = urljoin(BASE_URL, current_path)

        if full_url in visited_urls:
            continue

        print(f"Crawling: {full_url}")
        print(f"Waiting {POLITENESS_DELAY} seconds (Politeness Window)...")
        time.sleep(POLITENESS_DELAY) 

        try:
            response = requests.get(full_url)
            if response.status_code != 200:
                print(f"Failed to fetch {full_url}. Status code: {response.status_code}")
                continue

            visited_urls.add(full_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all readable text from the page
            text_content = soup.get_text(separator=' ', strip=True)
            pages_data[full_url] = text_content

            # Find the 'Next' page button and add to queue
            next_button = soup.select_one('.next > a')
            if next_button:
                url_queue.append(next_button['href'])

        except Exception as e:
            print(f"Error crawling {full_url}: {e}")

    return pages_data