import requests
import json
# WooCommerce API endpoint and authentication credentials
website = "https://www.best-brandlimited.co.uk" #replace it with your website domain

consumer_key = "ck_296f3d38292b02e16ca67b12ddf9849d2050de0d" # your consumer key(can get on WP WooCommerce Setting)
consumer_secret = "cs_b58127f0ef657d3a2a374419676f44da92f050d4" #your consumer secret


def get_all_categories():
    # Endpoint for getting all categories
    endpoint = f"{website}/wp-json/wc/v3/products/categories"

    # Set up the authentication parameters
    auth = (consumer_key, consumer_secret)

    # Make the request to the WooCommerce API
    page = 1
    all_categories = []

    while True:
        # Set the page parameter in the request
        params = {'page': page}

        # Make the request to the WooCommerce API
        response = requests.get(endpoint, auth=auth, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            categories = response.json()

            # If there are no more categories, break the loop
            if not categories:
                break

            # Extend the list of categories
            all_categories.extend(categories)

            # Move to the next page
            page += 1
        else:
            # Print an error message if the request was not successful
            #print(f"Error: {response.status_code}, {response.text}")
            return None

    # Extract category names
    category_names = [{'name':category['name'],'id':category['id']} for category in all_categories]

    return category_names


# Send a POST request to create the product
def wc_import(data):
    url = f"{website}/wp-json/wc/v3/products"
    response = requests.post(url, auth=(consumer_key, consumer_secret), json=data)

    # Check if the request was successful
    if response.status_code == 201:
        print("Product created successfully.")
        product = response.json()
        return product['id']
    else:
        print("Failed to create the product. Status code:", response.status_code)
        print("Response content:", response.text)

#Add variation to the product
def variation_import(product_id,data):
    url = f"{website}/wp-json/wc/v3/products/{product_id}/variations/batch"
    response = requests.post(url, auth=(consumer_key, consumer_secret), json=data)
    if response.status_code == 200:
        print("Variation created successfully.")
        product = response.json()
        return product['id']
    else:
        print("Failed to create the Variation. Status code:", response.status_code)
        print("Response content:", response.text)