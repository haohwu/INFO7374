import requests
from bs4 import BeautifulSoup
import json

def scrape_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return None

def extract_text(soup, selector):
    element = soup.select_one(selector)
    return element.get_text(strip=True) if element else "Information not available"

base_url = 'https://www.toro-restaurant.com'
pages = ['', '/menus', '/about', '/hours-location-index', '/events-1', '/employment-index', '/reservations']
selectors = {
    '/menus': '.menus .menu-item-title span .menu-item-price-top span .menu-item-description span .menu-item-price-bottom span'
}


data = {}
for page in pages:
    url = f"{base_url}{page}"
    soup = scrape_url(url)
    if soup:
        selector = selectors.get(page, 'div > p')  
        data[page] = extract_text(soup, selector)

with open('data.json', 'w') as f:
    json.dump(data, f)



