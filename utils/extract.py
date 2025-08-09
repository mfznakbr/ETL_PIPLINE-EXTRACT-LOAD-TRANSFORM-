import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime


HEADERS = {
    "User-Agent" : (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

class Extract:
    def __init__(self, base_url):
        self.base_url = base_url


    def scrape(self, url):
        """Scrape data from the fashion product pages."""
        sesi = requests.Session()
        response = sesi.get(self.base_url, headers=HEADERS)

        try:
         # Check for HTTP errors
            return response # Get the content of the page
        except requests.exceptions.RequestException as exp:
            print(f"Error when sending a requests: {exp}")
            return None
    
    def extract_data(self, product):
        """
        Extract data from the product details.
        """     
        data_default = {
            "Title": "not available",
            "Price": "not available",
            "Rating": "not available",
            "Colors": "not available",
            "Size": "not available",
            "Gender" : "not available"
        }

        try:
            # Extract title
            title_elem = product.find('h3', class_='product-title')
            title = title_elem.text.strip() if title_elem else data_default["Title"]
            
            # Extract price
            price = data_default["Price"]
            price_container = product.find('div', class_='price-container')

            if price_container:
                price_elem = price_container.find('span', class_='price')
                if price_elem:
                    price = price_elem.text.strip()

            # Extract raing, colors, and size
            p_elems = product.find_all('p', style="font-size: 14px; color: #777;")
            attributes = {
                "Rating": data_default["Rating"],
                "Colors": data_default["Colors"],
                "Size": data_default["Size"],
                "Gender": data_default["Gender"]
            }
            
            for i, key in enumerate(attributes.keys()):
                if i < len(p_elems):
                    attributes[key] = p_elems[i].text.strip()
                    
            return {
                "Title": title,
                "Price": price,
                **attributes,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"Error during extraction: {e}")
            return data_default
        
    def fetching_content(self, start_page=1, delay=2):
        """
        Fetch content from the given URL.
        """
        max_pages = 50
        data = []

        try:
            for page in range(start_page, max_pages + 1):
                url = f"{self.base_url.rstrip('/')}/page{page}" if page > 1 else self.base_url
                print(f"\nFetching page {page}: {url}")
                
                response = self.scrape(url)
                response.raise_for_status()

                if not response.content:
                    print("Failed to fetch content")
                    break
                soup = BeautifulSoup(response.content, "html.parser")
                product_fashion = soup.find_all('div', class_='product-details')

                if not product_fashion:
                    print("No products found")
                    break
                print(f"Found {len(product_fashion)} products")
                for i, product in enumerate(product_fashion, 1):
                    product_data = self.extract_data(product)
                    print(f"{i}. {product_data['Title']} == {product_data['Price']}")
                    data.append(product_data)

                next_btn = soup.find('li', class_='page-item next')
                if not next_btn or 'disabled' in next_btn.get('class', []):
                    print("⏹️ No next page")
                    break
                time.sleep(delay)
            return data
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return None
        
        