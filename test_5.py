import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# -------------------------------
# Step 1: Base URL and headers
# -------------------------------
base_url = "https://www.flipkart.com/mobiles/pr?sid=tyy,4io&page="
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}

# -------------------------------
# Step 2: Pagination variables
# -------------------------------
page = 1
data = []

# -------------------------------
# Step 3: Loop through pages
# -------------------------------
while page < 6:  
    print(f"\n🔍 Scraping Page {page}")
    url = base_url + str(page)
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to load page")
        break

    soup = BeautifulSoup(response.text, "lxml")

    # Find product blocks
    product_blocks = soup.find_all("div", class_="lvJbLV")
    print(f"Found {len(product_blocks)} product blocks on page {page}")

    # Stop if no products found
    if not product_blocks:
        print("No more products found. Stopping pagination.")
        break

    # -------------------------------
    # Step 4: Extract product data
    # -------------------------------
    for product in product_blocks:
        # Name
        name_tag = product.find("div", class_="RG5Slk")
        if not name_tag:
            continue
        name = name_tag.text.strip()

        # Price
        price_tag = product.find("div", class_="hZ3P6w DeU9vF")
        price = price_tag.text.strip() if price_tag else "N/A"

        # Description
        desc_tag = product.find("ul", class_="HwRTzP")
        description = (
            " | ".join(li.text.strip() for li in desc_tag.find_all("li", class_="DTBslk"))
            if desc_tag else "N/A"
        )

        # Debug print
        print("DEBUG:")
        print("Name:", name)
        print("Price:", price)
        print("Description:", description)
        print("-" * 100)

        # Store data
        data.append({
            "Name": name,
            "Price": price,
            "Description": description
        })

    # Move to next page
    page += 1

    # For not loading the server too fast
    time.sleep(5)

# -------------------------------
# Step 5: Save all data to CSV
# -------------------------------
pd.DataFrame(data).to_csv("flipkart_products_all_pages.csv", index=False)
print("\n✅ Data saved to flipkart_products_all_pages.csv")
