import urllib.parse
import urllib.request
import requests
from bs4 import BeautifulSoup
import sys

import time
import json
import urllib3
import codecs
import random


#Function for finding our desired item and size on shopify store
def find_prod_shopify(item, size):
    #Initialise our session
    session = requests.session()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    #Take a json from the shopify site containing a list of all products and
    #their variants (size & colourways etc.). This is consisten across all sites
    #that use shopify.
    url = 'https://bapeonline.com' + '/products.json'
    r = session.get(url, verify=False)
    products_json = json.loads(r.text)
    products = products_json["products"]

    #Find the product we're looking for
    for product in products:
        if(item.upper() == product['title'].upper()):
            prod = product

    #Find the product id of our product in the desired size. If size unavailable
    #last size in list is selected.
    size_found = 0
    for variant in prod['variants']:
        if size in variant['title']:
            var = str(variant['id'])
            size_found == 1;
        else
            var_temp = str(variant['id'])

    if size_found == 0:
        var = var_temp






find_prod_shopify('SHARK WIDE PULLOVER HOODIE')


