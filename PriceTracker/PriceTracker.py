from bs4 import BeautifulSoup
import requests
from datetime import datetime

url = "https://www.computersalg.dk/i/24105172/msi-geforce-rtx-5070-12g-ventus-2x-oc-grafikkort-geforce-rtx-5070-12-gb-gddr7-pci-express-5-0-3-x-displayport-hdmi"

print("getting page...")

headers = {"User-Agent": "Mozilla/5.0"}
soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")

price = (
    soup.find(attrs={"itemprop": "price"}) and soup.find(attrs={"itemprop": "price"}).get("content")
    or soup.find(class_="v-product-details__price") and soup.find(class_="v-product-details__price").text.strip()
    or soup.find("meta"
                 , {"property": "product:price:amount"}) and soup.find("meta", {"property": "product:price:amount"}).get("content")
)

if price:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Price:", price)

    with open("prices.txt", "a") as f:
        f.write(f"{now} - {price}\n")

    print("saved!")
else:
    print("couldn't find price :(")
