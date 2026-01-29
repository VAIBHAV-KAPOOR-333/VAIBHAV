import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# -------------------------------
# Step 1: URL & Headers
# -------------------------------
url = "https://www.flipkart.com/mobiles/pr?sid=tyy,4io"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}

# -------------------------------
# Step 2: Fetch page
# -------------------------------
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Failed to load page!")
    exit()

print("Status Code:", response.status_code)

# -------------------------------
# Step 3: Parse HTML
# -------------------------------
soup = BeautifulSoup(response.text, "lxml")

# -------------------------------
# Step 4: Find all products
# -------------------------------
products = soup.find_all("div", class_="jIjQ8S")
print("Total products found:", len(products))

# -------------------------------
# Step 5: Extract data
# -------------------------------
data = []

for idx, product in enumerate(products, start=1):
    # ----- Name -----
    name = product.find("div", class_="RG5Slk")
    name = name.text.strip() if name else "N/A"

    # ----- Price -----
    price = product.find("div", class_="hZ3P6w")
    price = price.text.strip() if price else "N/A"

    # ----- Image -----
    img = product.find("img", class_="UCc1lI")
    image_url = img["src"] if img else "N/A"

    # ----- Rating -----
    rating = product.find("div", class_="MKiFS6")
    rating = rating.text.strip() if rating else "N/A"

    # ----- Ratings & Reviews -----
    reviews_tag = product.find("span", class_="PvbNMB")
    ratings_count = reviews_count = "N/A"
    if reviews_tag:
        text = reviews_tag.text
        ratings_match = re.search(r"([\d,]+)\sRatings", text)
        reviews_match = re.search(r"([\d,]+)\sReviews", text)
        ratings_count = ratings_match.group(1) if ratings_match else "N/A"
        reviews_count = reviews_match.group(1) if reviews_match else "N/A"

    # ----- Description -----
    desc_list = product.find("ul", class_="HwRTzP")
    description = " | ".join(li.text.strip() for li in desc_list.find_all("li", class_="DTBslk")) if desc_list else "N/A"

    # ----- Debug Print -----
    print(f"\nProduct {idx}")
    print("Name:", name)
    print("Price:", price)
    print("Rating:", rating)
    print("Ratings Count:", ratings_count)
    print("Reviews Count:", reviews_count)
    print("Image URL:", image_url)
    print("Description:", description)
    print("-" * 60)

    # ----- Add to data -----
    data.append({
        "Name ": name ,
        "Price ": price ,
        "Rating ": rating ,
        "Ratings Count ": ratings_count ,
        "Reviews Count ": reviews_count ,
        "Image URL ": image_url ,
        "Description ": description
    })

# -------------------------------
# Step 6: Save to CSV
# -------------------------------
pd.DataFrame(data).to_csv("flipkart_products_simplified.csv", index=False)
print("\nData saved to flipkart_products_simplified.csv")
