import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com/"
response = requests.get(url)

if response.status_code != 200:
    print("Failed to load page")
    exit()

soup = BeautifulSoup(response.text, "lxml")
quotes = soup.find_all("span", class_="text")

with open("quotes.txt", "w", encoding="utf-8") as file:
    for quote in quotes:
        file.write(quote.text + "\n")

print("Scraping complete. Data saved to quotes.txt")
