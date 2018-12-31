import urllib.parse
import urllib.request
import requests
from bs4 import BeautifulSoup
import timeit

'-------Info-------'
#base_url take as input argument
#key search product terms as input argument
#desired size as input argument

search_delay = 1

#Checkout settings PREFERABLY SETUP A GUI
email = ''
fname = ''
lname = ''

addl_1 = ''
addl_2 = ''
city = ''
country = ''
post_code = ''
phone = ''

#Payment details
card_num = ''
cardholder = ''
exp_m = ''
exp_y = ''
cvv = ''

session = requests.session()

def bape():
    # url = 'https://us.bape.com/collections/collaboration'
    url = 'https://us.bape.com' + 'products.json'
    item = 'BAPE X DR.MARTENS ABC 3 HOLE STEEL TOE CAP SHOES LADIES'.upper()
    f = urllib.request.urlopen(url)
    script = BeautifulSoup(f, "lxml")
    for link in script.find_all('a'):
        if link.get('title') == item:
            prod = link.get('href')

    url = 'https://us.bape.com' + prod
    f = urllib.request.urlopen(url)
    script = BeautifulSoup(f, "lxml")
    print(script)
    return

start = timeit.timeit()
bape()
end = timeit.timeit()
print(end - start)
