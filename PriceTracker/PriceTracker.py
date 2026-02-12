import requests
from bs4 import BeautifulSoup
from datetime import datetime

# websites to track
#just defined the websites in a list of dictionariess
websites = [
    {
        'name': 'Computersalg.dk',
        'product_name': 'MSI GeForce RTX 5070 12G VENTUS 2X OC',
        'url': 'https://www.computersalg.dk/i/24105172/msi-geforce-rtx-5070-12g-ventus-2x-oc-grafikkort-geforce-rtx-5070-12-gb-gddr7-pci-express-5-0-3-x-displayport-hdmi',
        'method': 'itemprop'
    },
    {
        'name': 'elgiganten.dk',
        'product_name': 'MSI GeForce RTX 5070 12G VENTUS 2X OC grafikkort',
        'url': 'https://www.elgiganten.dk/product/gaming/pc-komponenter/grafikkort-gpu/msi-geforce-rtx-5070-12g-ventus-2x-oc-grafikkort/900914?utm_content=all&utm_strategy=pricerunner&utm_source=pricerunner&utm_medium=cpc&utm_campaign=pricerunner',
        'method': '-mt-[6px] font-headline text-[3.5rem] leading-[3.5rem] justify-self-start'
    }
]

for site in websites:
    print(f"Checking {site['name']}...")
    
    page = requests.get(site['url'], headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(page.content, 'html.parser')
    
    price = None
    
    
    if site['method'] == 'itemprop':
        price_element = soup.find(attrs={'itemprop': 'price'})
        if price_element:
            price = price_element.get('content')
            price = price.strip()
    
    #finds the price based on the class name 
    elif site['method'] == '-mt-[6px] font-headline text-[3.5rem] leading-[3.5rem] justify-self-start':
        price_element = soup.find(class_='-mt-[6px] font-headline text-[3.5rem] leading-[3.5rem] inc-vat')
        if price_element:
            price = price_element.text.strip()
    
    if price:
        current_time = datetime.now()
        time_string = current_time.strftime('%Y-%m-%d %H:%M:%S')
        
        file = open('prices.txt', 'a')
        message = site['name'] + " - " + site['product_name'] + " - " + price + " - " + time_string + "\n" 
        file.write(message)
        file.close()
        
        print("Price found: " + price)
    else:
        print("Price not found")
    
    print("")