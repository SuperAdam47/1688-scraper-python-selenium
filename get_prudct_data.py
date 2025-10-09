#This script is for development test use to get product data by id
import requests
from requests.auth import HTTPBasicAuth
# get product data
# WooCommerce API credentials
consumer_key = "ck_296f3d38292b02e16ca67b12ddf9849d2050de0d"
consumer_secret = "cs_b58127f0ef657d3a2a374419676f44da92f050d4"

# WooCommerce API endpoint for products
product_id = 1022065
url = f"https://www.best-brandlimited.co.uk/wp-json/wc/v3/products/{product_id}"

# Make the API request
response = requests.get(
    url,
    auth=HTTPBasicAuth(consumer_key, consumer_secret), # You can adjust the query parameters as needed
)



# Check the response
if response.status_code == 200:
    products = response.json()
    products.pop('description')
    print(products)
    
else:
    print(f"Failed to fetch products. Status code: {response.status_code}, Response: {response.text}")
