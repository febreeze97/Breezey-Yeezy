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
def find_prod_shopify(site, item, size):
    #Initialise our session
    session = requests.session()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    #Take a json from the shopify site containing a list of all products and
    #their variants (size & colourways etc.). This is consisten across all sites
    #that use shopify.
    url = site + '/products.json'
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
            size_found = 1;
        else:
            var_temp = str(variant['id'])

    if size_found == 0:
        var = var_temp

    #cart_link offers a url to redirect to a cart with the items you want for an enhanced manual cop
    cart_link = site + '/cart/' + var + ':1'
    #add_to_cart adds our items to cart for session via backend
    add_to_cart = site + '/cart/add.js?quantity=1&id=' + var
    response = session.get(add_to_cart, verify = False)
    # print(response.cookies)
    shipping = shopify_shipping(site, session, 'NN13 5NP', 'United Kingdom', response.cookies)


def shopify_payment():
    link = 'https://elb.deposit.shopifyycs.com/sessions'
    #create a json of our payment details
    pay_load = {
        'credit_card': {
            "number": '1234567890123456',
            "name": 'Mr. G',
            "month": '03',
            "year": '21',
            "verification_value": '666'
        }
    }
    r = requests.post(link, json=pay_load, verify = False)

    #Create a payment token
    token = json.loads(r.text)['id']

    return token

def shopify_shipping(site, session, post_code, country, cj):
    #Details required for shopify to calculate shipping costs
    link = site + '//cart/shipping_rates.json?shipping_address[zip]=' + post_code + '&shipping_address[country]=' + country
    r = session.get(link, cookies=cj, verify = False)
    shipping_opts = json.loads(r.text)

    ship_opt = shipping_opts['shipping_rates'][0]['name'].replace(' ', '%20')
    ship_price = shipping_opts['shipping_rates'][0]['price']

    shipping_option = 'shopify-' + ship_opt + '-' + ship_price

    return shipping_option

def submit_shopify_info(site, session, email, fname, lname, addl_1, addl_2, city, post_code, phone, cj):

    #All of our shipping details
    payload = {
        'utf8': u'\u2713',
        '_method': 'patch',
        'authenticity_token': '',
        'previous_step': 'contact_information',
        'step': 'shipping_method',
        'checkout[email': email
        'checkout[buyer_accepts_marketing': '0',
        'checkout[shipping_address][first_name': fname,
        'checkout[shipping_address][last_name':lname,
        'checkout[shipping_address][company]': '',
        'checkout[shipping_address][address1]': addl_1,
        'checkout[shipping_address][address2]':addl_2,
        'checkout[shipping_address][city]': city,
        'checkout[shipping_address][province]': '',
        'checkout[shipping_address][zip]': post_code,
        'checkout[shipping_address][phone]': phone,
        'checkout[remember_me]': '0',
        'checkout[client_details][browser_width]': '1710',
        'checkout[client_details][browser_height]': '1289',
        'checkout[client_details][javascript_enabled]': '1',
        'button': ''
    }

    #Generate a checkout link
    link = site + '//checkout.json'
    response = session.get(link, cookies = cj, verify = False)

    checkout_link = response.url

    #Send our data to checkout
    response = session.post(link, cookies = cj, data=payload, verify=False)

    return(response, checkout_link)




find_prod_shopify('https://bapeonline.com', 'SHARK WIDE PULLOVER HOODIE', "BLACK / M (MEN'S)")