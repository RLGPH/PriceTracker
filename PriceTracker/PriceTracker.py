import requests
from bs4 import BeautifulSoup
Simon_NewTest
from datetime import datetime, timezone
import schedule
import time

API_URL = "http://localhost:32777/api/scraper"

from datetime import datetime
import schedule
import time

API_URL = "http://localhost:32777/api/scraper"


# websites to track
websites = [
   {
       'name': 'Computersalg.dk',
       'url': 'https://www.computersalg.dk/i/24105172/msi-geforce-rtx-5070-12g-ventus-2x-oc-grafikkort-geforce-rtx-5070-12-gb-gddr7-pci-express-5-0-3-x-displayport-hdmi',
       'method': 'itemprop',
       'product_name': 'MSI GeForce RTX 5070 12G VENTUS 2X OC grafikkort'
   },
   {
       'name': 'elgiganten .dk',
       'url': 'https://www.elgiganten.dk/product/gaming/pc-komponenter/grafikkort-gpu/msi-geforce-rtx-5070-12g-ventus-2x-oc-grafikkort/900914?utm_content=all&utm_strategy=pricerunner&utm_source=pricerunner&utm_medium=cpc&utm_campaign=pricerunner',
       'method': '-mt-[6px] font-headline text-[3.5rem] leading-[3.5rem] justify-self-start',
       'product_name': 'MSI GeForce RTX 5070 12G VENTUS 2X OC grafikkort'
   }
]

def parse_price(raw: str) -> float | None:
    if not raw:
        return None
    cleaned = raw.replace("kr", "").replace(",-", "").replace("DKK", "").strip()
    # removing dash
    cleaned = cleaned.rstrip('-').rstrip(',').rstrip('.').strip()
    # replace comma with dot 
    cleaned = cleaned.replace('.', '').replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        print(f"  [!] Could not parse price: '{raw}'")
        return None

def check_prices():
   current_time = datetime.now().isoformat()
   print(f"\n--- Running price check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
   for site in websites:
       print(f"Checking {site['name']}...")
       try:
           page = requests.get(site['url'], headers={'User-Agent': 'Mozilla/5.0'})
           soup = BeautifulSoup(page.content, 'html.parser')
           price = None


           if site['method'] == 'itemprop':
               price_element = soup.find(attrs={'itemprop': 'price'})
               if price_element:
                   price = parse_price(price_element.get('content').strip())


           elif site['method'] == '-mt-[6px] font-headline text-[3.5rem] leading-[3.5rem] justify-self-start':
               price_element = soup.find(class_='-mt-[6px] font-headline text-[3.5rem] leading-[3.5rem] inc-vat')
               if price_element:
                   price = parse_price(price_element.text.strip())

           if price:
             payload = {
                   "product": {
                       "vendorName": site['name'],
                       "produktName": site['product_name'],
                       "vendorUrl": site['url']
                   },
                  "price":{
                      "productID":0,
                      "price":price,
                      "retrivalDateTime":current_time
                  }
            }
             response = requests.post(API_URL, json=payload)
             print(f"Price found: {price} — API response: {response.status_code}")
           else:
                print("Price not found")

       except Exception as e:
           print(f"Error checking {site['name']} - {e}")

# It will check 08:00 in the morning and 20:00 in the evening every day
schedule.every().day.at("08:00").do(check_prices)
schedule.every().day.at("20:00").do(check_prices)


# run in the startup to get an immediate price check
check_prices()


print("Scheduler running. Checks at 08:00 and 20:00 daily. You can obviously stop the loop by pressing Ctrl+C.\n")
while True:
   schedule.run_pending()
   time.sleep(60)
