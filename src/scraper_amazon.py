import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from bs4 import BeautifulSoup
from product import Product
from utils.clean_price import clean_price


def scrape_amazon_sg(search_query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    search_query = search_query.replace(' ', '+')
    url = f"https://www.amazon.sg/s?k={search_query}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve Amazon data: Status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    products = []
    results = soup.find_all('div', {'data-component-type': 's-search-result'})[:5]
    rank = 1

    for item in results:
        try:
            name_tag = item.h2
            name = name_tag.text.strip() if name_tag else "Product name not found"

            link_tag = item.find('a', class_='a-link-normal', href=True)
            link = "https://www.amazon.sg" + link_tag['href'] if link_tag else "Link not available"

            price_whole = item.find('span', class_='a-price-whole')
            price_fraction = item.find('span', class_='a-price-fraction')
            if price_whole and price_fraction:
                whole = price_whole.text.replace(',', '').strip()
                fraction = price_fraction.text.strip()
                if whole.endswith('.'):
                    whole = whole.rstrip('.')
                price = f"{whole}.{fraction}"
            else:
                price = "Price not available"

            image_tag = item.find('img', class_='s-image')
            image_url = image_tag['src'] if image_tag else "Image not available"

            cleaned_price = clean_price(price)

            product = Product('Amazon', name, cleaned_price, link, image_url, rank)
            products.append(product)
            rank += 1
        except Exception as e:
            print(f"Error extracting product data: {e}")
            continue

    return products


if __name__ == "__main__":
    query = input("Enter a product to search on Amazon SG: ")
    results = scrape_amazon_sg(query)
    if results:
        for idx, product in enumerate(results, 1):
            print(f"\nProduct {idx}:")
            print(f"Platform: {product.platform}")
            print(f"Name: {product.name}")
            print(f"Price: {product.price}")
            print(f"Link: {product.link}")
            print(f"Image URL: {product.image_url}")
    else:
        print("No products found or there was an error scraping data.")
