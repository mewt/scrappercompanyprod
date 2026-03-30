import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin
import re
import time
import logging

logger = logging.getLogger(__name__)

# --- Configuration Constants ---
SEARCH_BASE_URL = os.environ.get("SEARCH_BASE_URL", "https://companieshouse.id/search?term=")
BASE_DOMAIN = os.environ.get("BASE_DOMAIN", "https://companieshouse.id")
RATE_LIMIT = float(os.environ.get("RATE_LIMIT", "1"))  # seconds between requests
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "10"))  # seconds for request timeout

# Headers to mimic a browser request
HEADERS = {
    "User-Agent": os.environ.get("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"),
    "Accept": "text/html",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

# Fields to extract from the detail page
TARGET_FIELDS = [
    "Registered Name",
    "Legal Entity Type",
    "Business Number",
    "Registered Address",
    "City"
]

# --- Helper Function for Flexible Matching ---

def standardize_name(name):
    """
    Removes periods, commas, converts to lowercase, and strips whitespace
    to allow for flexible matching between user input and link text.
    """
    # Remove all periods and commas, then strip whitespace and convert to lowercase
    return name.replace('.', '').replace(',', '').strip().lower()

# --- Scraping Functions ---

def scrape_detail_page(detail_url):
    """
    Fetches and scrapes the company details from a specific profile page URL
    using robust HTML sibling traversal logic.
    """
    logger.info(f"Fetching detail page: {detail_url}")

    try:
        # Rate Limiting: Pause before making the request
        time.sleep(RATE_LIMIT)
        response = requests.get(detail_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        extracted_data = {}

        for field_name in TARGET_FIELDS:

            # 1. Find the <dt> tag that holds the label text (updated HTML structure)
            label_dt = soup.find('dt', string=field_name)

            if label_dt:
                # 2. Find the parent div and then find the <dd> within the same grid container
                parent_div = label_dt.find_parent('div', class_=lambda x: x and 'grid' in x)
                if parent_div:
                    value_dd = parent_div.find('dd')
                    if value_dd:
                        # Get the clean text from the value container
                        value = value_dd.get_text(strip=True)
                        extracted_data[field_name] = value
                    else:
                        extracted_data[field_name] = f"Value dd not found for {field_name}"
                else:
                    extracted_data[field_name] = f"Parent container not found for {field_name}"
            else:
                extracted_data[field_name] = f"Label not found for {field_name}"

        # Check for successful extraction
        if any("not found" not in v.lower() for v in extracted_data.values()):
             return extracted_data

        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error during detail request to {detail_url}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during detail request to {detail_url}: {str(e)}")
        return None


def extract_company_data(company_name):
    """
    Performs the two-step scrape: Search -> Find Link -> Scrape Detail Page.
    Uses standardized comparison for reliable link matching.
    """
    logger.info(f"Starting company data extraction for: {company_name}")
    
    search_url = SEARCH_BASE_URL + quote_plus(company_name)
    logger.info(f"Fetching search results URL: {search_url}")

    # Standardize the input name for a loose comparison
    standardized_input_name = standardize_name(company_name)

    try:
        # --- Step 1: Find the Detail Link from the Search Results ---
        # Rate Limiting: Pause before making the search request
        time.sleep(RATE_LIMIT)
        response = requests.get(search_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        search_soup = BeautifulSoup(response.content, 'html.parser')

        # Target the <a> tag by comparing the standardized input name to the standardized title attribute
        # The title attribute contains the exact company name (updated for new HTML structure)
        all_links = search_soup.find_all('a', href=True)
        target_link = None
        for link in all_links:
            title = link.get('title', '')
            if title and standardized_input_name == standardize_name(title):
                target_link = link
                break

        if not target_link:
            logger.warning(f"Company '{company_name}' not found as a standardized match in the search results.")
            return None

        relative_url = target_link.get('href')

        if not relative_url:
             logger.warning("Found company name but link (href) was missing.")
             return None

        # Create the absolute URL for the detail page
        detail_page_url = urljoin(BASE_DOMAIN, relative_url)
        logger.info(f"Found detail page URL: {detail_page_url}")

        # --- Step 2: Scrape the Detail Page ---
        result = scrape_detail_page(detail_page_url)
        if result:
            logger.info(f"Successfully extracted company data for '{company_name}'")
        else:
            logger.warning(f"Failed to extract company data for '{company_name}'")
        
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error during search request for '{company_name}': {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during search request for '{company_name}': {str(e)}")
        return None