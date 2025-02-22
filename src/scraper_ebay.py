import requests
from bs4 import BeautifulSoup

def scrape_ebay_sg(search_query):
    # Format the search URL for eBay Singapore
    search_query = search_query.replace(' ', '+')
    url = f"https://www.ebay.com.sg/sch/i.html?_nkw={search_query}&_sacat=0&_from=R40&_trksid=m570.l1313"

    # Send an HTTP GET request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve page with status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product listings
    products = []
    listings = soup.find_all("li", class_="s-item")

    if not listings:
        print("No products found.")
        return []

    for listing in listings[2:7]:  # Get only the top 10 products
        try:
            # Filter out irrelevant sponsored/advertisement items
            if listing.find('span', class_='s-item__ad-badge-text'):
                continue

            # Extract product name
            name_tag = listing.find("div", class_="s-item__title")
            name = name_tag.text.strip() if name_tag else "No name found"

            # Extract product price
            price_tag = listing.find("span", class_="s-item__price")
            price = price_tag.text.strip() if price_tag else "No price found"

            # Extract product link
            link_tag = listing.find("a", class_="s-item__link")
            link = link_tag.get("href") if link_tag else "No link found"

            # Extract product image URL
            img_tag = listing.find("img")
            image_url = img_tag.get("src") if img_tag else "No image found"

            # Append product details
            products.append({
                'name': name,
                'price': price,
                'link': link,
                'image_url': image_url,
            })

        except Exception as e:
            print(f"Error extracting product data: {e}")
            continue

    return products

# Test the scraper
if __name__ == "__main__":
    query = input("Enter a product to search on eBay SG: ")
    results = scrape_ebay_sg(query)
    if results:
        for idx, product in enumerate(results, 1):
            print(f"\nProduct {idx}:")
            print(f"Name: {product['name']}")
            print(f"Price: {product['price']}")
            print(f"Link: {product['link']}")
            print(f"Image URL: {product['image_url']}")
    else:
        print("No products found or there was an error scraping data.")
