from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import requests

# -------------------------------
# Setup Selenium Chrome driver
# -------------------------------
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--headless")  # comment if you want to see browser

driver = webdriver.Chrome(options=chrome_options)

# -------------------------------
# Step 1: Open Flipkart mobiles page
# -------------------------------
url = "https://www.flipkart.com/mobiles/pr?sid=tyy,4io"
driver.get(url)
time.sleep(2)

# Close login popup if it appears
try:
    close_btn = driver.find_element(By.XPATH, "//button[contains(text(),'✕')]")
    close_btn.click()
except:
    pass

# -------------------------------
# Step 2: Collect all product URLs
# -------------------------------
product_elements = driver.find_elements(By.CSS_SELECTOR, "div.jIjQ8S a._1fQZEK")
product_urls = [el.get_attribute("href") for el in product_elements]
print("Total products found:", len(product_urls))

# -------------------------------
# Prepare storage
# -------------------------------
data = []
images_folder = "images"
os.makedirs(images_folder, exist_ok=True)

# -------------------------------
# Step 3: Scrape each product
# -------------------------------
for idx, url in enumerate(product_urls, start=1):
    try:
        driver.get(url)
        time.sleep(2)  # wait for page load

        soup = BeautifulSoup(driver.page_source, "lxml")

        # ----- Name -----
        name_tag = soup.find("span", class_="B_NuCI")
        name = name_tag.text.strip() if name_tag else "N/A"

        # ----- Price -----
        price_tag = soup.find("div", class_="_30jeq3 _16Jk6d")
        price = price_tag.text.strip() if price_tag else "N/A"

        # ----- Rating -----
        rating_tag = soup.find("div", class_="_3LWZlK")
        rating = rating_tag.text.strip() if rating_tag else "N/A"

        # ----- Ratings & Reviews Count -----
        ratings_count_tag = soup.find("span", class_="_2_R_DZ")
        ratings_count = reviews_count = "N/A"
        if ratings_count_tag:
            text = ratings_count_tag.text
            if "Ratings" in text and "Reviews" in text:
                parts = text.split("&")
                ratings_count = parts[0].strip()
                reviews_count = parts[1].strip()

        # ----- Description -----
        desc_list = soup.find_all("li", class_="rgWa7D")
        description = " | ".join(li.text.strip() for li in desc_list) if desc_list else "N/A"

        # ----- Image -----
        img_tag = soup.find("img", class_="_396cs4 _2amPTt _3qGmMb")
        img_url = img_tag["src"] if img_tag else "N/A"

        # Download image
        if img_url != "N/A":
            img_data = requests.get(img_url).content
            img_path = os.path.join(images_folder, f"{idx}.jpg")
            with open(img_path, "wb") as f:
                f.write(img_data)

        # ----- Customer Reviews -----
        reviews = []
        try:
            # Click "Read all reviews" if exists
            read_all = driver.find_element(By.XPATH, "//div[contains(text(),'Read all')]")
            driver.execute_script("arguments[0].click();", read_all)
            time.sleep(2)
            soup_reviews = BeautifulSoup(driver.page_source, "lxml")
            review_tags = soup_reviews.find_all("div", class_="t-ZTKy")
            for r in review_tags:
                review_text = r.text.strip().replace("\n", " ")
                reviews.append(review_text)
        except:
            reviews.append("No reviews")

        # ----- Append data -----
        data.append({
            "Name": name,
            "Price": price,
            "Rating": rating,
            "Ratings Count": ratings_count,
            "Reviews Count": reviews_count,
            "Description": description,
            "Image URL": img_url,
            "Customer Reviews": " || ".join(reviews)
        })

        print(f"Scraped Product {idx}: {name}")

    except Exception as e:
        print(f"Error scraping product {idx}: {e}")

# -------------------------------
# Step 4: Save CSV
# -------------------------------
df = pd.DataFrame(data)
df.to_csv("flipkart_products_with_reviews.csv", index=False)
print("\nData saved to flipkart_products_with_reviews.csv")
print(f"Images saved in '{images_folder}/' folder")

# -------------------------------
# Close driver
# -------------------------------
driver.quit()
