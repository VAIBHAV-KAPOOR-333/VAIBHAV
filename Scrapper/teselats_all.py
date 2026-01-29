from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import pandas as pd
import time

# -------------------------------
# Step 1: Setup Chrome options
# -------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# -------------------------------
# Step 2: Base URL & variables
# -------------------------------
base_url = "https://www.flipkart.com/mobiles/pr?sid=tyy,4io&page="
page = 1
data = []

# -------------------------------
# Step 3: Pagination loop
# -------------------------------
while page < 42:
    print(f"\n🔍 Scraping Page {page}")
    driver.get(base_url + str(page))

    # Wait for page to load
    time.sleep(5)

    # Get fully rendered HTML
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Find product blocks
    product_blocks = soup.find_all("div", class_="lvJbLV")
    print(f"Found {len(product_blocks)} product blocks on page {page}")

    if not product_blocks:
        print("No more products found. Stopping pagination.")
        break

    # -------------------------------
    # Step 4: Extract product data
    # -------------------------------
    for product in product_blocks:
        # Product Name
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

        # Debug output
        print("DEBUG:")
        print("Name:", name)
        print("Price:", price)
        print("Description:", description)
        print("-" * 100)

        data.append({
            "Name": name,
            "Price": price,
            "Description": description
        })

    page += 1

    # Polite delay
    time.sleep(5)

# -------------------------------
# Step 5: Save data
# -------------------------------
pd.DataFrame(data).to_csv("flipkart_products_all_pages_selenium.csv", index=False)
print("\n✅ Data saved to flipkart_products_all_pages_selenium.csv")

# -------------------------------
# Step 6: Close browser
# -------------------------------
driver.quit()
