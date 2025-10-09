import os
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from googletrans import Translator  # module for translation
from currency_converter import CurrencyConverter  # module for currency convert
import csv
from importer import wc_import, variation_import, get_all_categories
"""
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from datetime import datetime, timedelta

"""


def init_uc():  # initialize undeteced chromedriver
    options = uc.ChromeOptions()
    _driver = uc.Chrome(driver_executable_path='./chromedriver.exe', options=options, version_main=118)

    return _driver


def get_batch(text):  # extract numbers from head of string.
    for i in range(len(text)):
        try:
            n = int(text[i])
        except:
            break

    return float(text[:i])


def get_delivery_time(text):
    for i in text:
        x = ""
        temp = i.text
        if len(temp) >= 3:
            x += temp[2]
        if len(temp) >= 4:
            x += temp[3]
        if x == "48":
            return x
    return "0"


# function for login
def login(user_name, password):
    driver.find_element(By.ID, 'fm-login-id').click()
    sleep(.5)
    driver.find_element(By.ID, 'fm-login-id').send_keys(user_name)

    sleep(1)

    driver.find_element(By.ID, 'fm-login-password').click()

    driver.find_element(By.ID, 'fm-login-password').send_keys(password)

    sleep(1)

    driver.find_element(By.CLASS_NAME, 'fm-submit').click()

    sleep(10)


def get_sku(url):
    a = url.index('/offer')
    b = url.index('.html')
    return url[a + 7:b]


def write_headers_once(filename, headers): #chcek if csv exist for first time to write headers
    file_exists = os.path.isfile(filename)
    if not file_exists:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()


def add_row(filename, row): #writes rows to csv
    headers = ['name', 'regular_price', 'categories', 'sku', 'images', 'video', 'description', 'additional_information',
               'reviews', 'attributes', 'type', 'colors']

    write_headers_once(filename, headers)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerow(row)
        print("Item added to csv")


def remove_external_links(html_content): #remove external links from description
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find and remove all 'a' tags within the element
    for tag in soup.find_all(attrs={'href': True}):
        del tag['href']

    # Get the modified HTML content
    return str(soup)


def get_price(price):
    return float(price[1:])


def amazon_price(image_url): #to get product price from amazon using googlelens
    #print(image_url)
    pr_f = 0.0
    options = uc.ChromeOptions()
    driver1 = uc.Chrome(driver_executable_path='./chromedriver.exe', options=options, version_main=118)
    image_to_search = image_url
    driver1.get("https://google.co.uk")
    driver1.find_element(By.CLASS_NAME, "Gdd5U").click()
    sleep(12)
    driver1.find_element(By.CLASS_NAME, "cB9M7").click()
    driver1.find_element(By.CLASS_NAME, "cB9M7").send_keys(image_to_search)
    driver1.find_element(By.CLASS_NAME, "Qwbd3").click()
    sleep(3)
    all_links = driver1.find_elements(By.CLASS_NAME, "ksQYvb")
    #print(len(all_links))
    for link in all_links:
        try:
            #print(l.find_element(By.CLASS_NAME, "fjbPGe").text)
            if link.find_element(By.CLASS_NAME, "fjbPGe").text == "Amazon UK":
                link.click()
        except:
            continue
    sleep(5)
    if driver1.window_handles[-1] == driver1.window_handles[0]:
        driver1.close()
    else:
        driver1.switch_to.window(driver1.window_handles[-1])
        while True:
            try:
                pr = get_price(driver1.find_element(By.CSS_SELECTOR,
                                               "span.a-price.a-text-price.a-size-medium span.a-offscreen").get_attribute(
                    "innerText"))
                if pr < pr_f or pr_f == 0.0:
                    pr_f = pr
            except:
                pass
            driver1.close()
            driver1.switch_to.window(driver1.window_handles[-1])
            if driver1.window_handles[-1] == driver1.window_handles[0]:
                break
        driver1.close()
    return pr_f


driver = init_uc()
file_name = 'scraped_data.csv'
c = CurrencyConverter()

exchange_rate = c.convert(1, 'CNY', 'GBP')  # get excahnge rate of CNY to GBP
exchange_rate_euro = c.convert(1, 'EUR', 'GBP')
print(f'Today"s rate is 1RMB : {exchange_rate:.3f} GBP')


# Initialize the Translator

def translate_to_en(text_to_translate):
    translator = Translator()
    end = 0
    translated_text = ''
    while end < len(text_to_translate):  # loop with 500 characters (limit count of translator)
        translated_text += translator.translate(text_to_translate[end:end + 500], dest='en').text
        end = end + 500
    return translated_text


categories = get_all_categories()

driver.get('https://1688.com')
# it's very important. You need to update this with your cookie data to bypass login
# Plz check readme to learn how to extract cookies from web browser
cookie_dict = {
    'cookie2': '104a0dc27df1d92c19f5f1997594ee15',
    't': 'f78b2e125ed08fbdb38d66b550d1bc47',
    '_tb_token_': '711bfee883513',
    'cna': 'c6PMHaiUBwkCAW3GB0Vhn5tU',
    'XSRF-TOKEN': '17129d05-0271-461b-a7f6-21eb773956ea',
    'xlly_s': '1',
    'cookie1': 'WqUNDVgfUjZEgjdAeHflnzulN5ssmCW9uDaXdmSeE3g%3D',
    'cookie17': 'UUphzOvA3RGzsVEBbw%3D%3D',
    'sgcookie': 'E100dhj76fufqF2ZlIc2UwEuJvVOpSVkJQJhhXVixuCgiNYeX1mSgi1wT%2Bvdy0GhDxf7OQkwKMbDtxhLeWaJXhJ%2F0giYZF1S0PBsKDx8IZceKKw%3D',
    'sg': '106',
    'csg': '04f86cef',
    'lid': 'posh111',
    'unb': '2206955801560',
    'uc4': 'nk4=0%40EbL%2BqZphOMFCnqD2ZPvDBUN%2F&id4=0%40U2grF8CMYg6Hz3zPRpoXawSI8kphaiQZ',
    '__cn_logon__': 'true',
    '__cn_logon_id__': 'posh111',
    'ali_apache_track': 'c_mid=b2b-22069558015606e1d8|c_lid=posh111|c_ms=1',
    'ali_apache_tracktmp': 'c_w_signed=Y',
    '_nk_': 'posh111',
    'last_mid': 'b2b-22069558015606e1d8',
    '_csrf_token': '1699628717658',
    '__mwb_logon_id__': 'posh111',
    '_m_h5_tk': '22f2ae0923f372ac9d0d6cb7ab435dab_1699655440808',
    '_m_h5_tk_enc': '5f1c05292443e839dc9ca511eb8f2add',
    'mwb': 'ng',
    'aliwwLastRefresh': '1699073813666',
    'is_identity': 'buyer',
    '_is_show_loginId_change_block_': 'b2b-22069558015606e1d8_false',
    '_show_force_unbind_div_': 'b2b-22069558015606e1d8_false',
    '_show_sys_unbind_div_': 'b2b-22069558015606e1d8_false',
    '_show_user_unbind_div_': 'b2b-22069558015606e1d8_false',
    'tfstk': 'dpik21jGK4z7VSNo5QEW4Ld6FG8An_ZQGXIL9kFeuSPjv4FpPHv3iJbFTMkUtXcYG73pdLaEiR2LUJSUaSW4QRWzLvoLLDcb4yg897F3xvGMHCK9XYM7AlR96hISKYZQboHFyhHSFk6lTd32XM0X0YBy8hXjEioCGyNGdFNExOjQH5kzgXhK08fT_YPcYMP4EOlOuN5KsMw2pm7CRzybn5EFzM-h.',
    'l': 'fBruao9nPYRt2PHkBOfaFurza77OSIRYSuPzaNbMi9fP9wsW5zw1W1FeGUvXC3MNFsMkR3RxBjFXBeYBqBAnnxv9SYRKwbHmnmOk-Wf..',
    'isg': 'BFRUK_BwzUnlu1kOK6MQ-ub8JZLGrXiXBwnj9e414F9j2fQjFr1IJwpT2cnBJLDv',
    '__rn_alert__': 'false',
    'taklid': '54741a6156c34b2b994ef0d87f3b0427'
}
cookies = []
for c in cookie_dict:
    cookies.append({
        'name': c,
        'value': cookie_dict[c],
        'domain': '.1688.com',
        'path': '/'
    })

for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()

sleep(.5)

# your 1688 account credentials

username = 'posh111'

password = 'abc123ABC!@#'

# the supplier url to be given.
# example url
# url = 'https://pintimewatchs.1688.com/page/offerlist.htm?spm=0.0.wp_pc_common_topnav_38229151.0'
url = input("Please insert url of 1688.com supplier")

#driver.get('https://login.taobao.com')
#login(username, password)

driver.get(url)

results = []
x = 0


while True:  # loop in all pages
    images = driver.find_elements(By.CLASS_NAME, 'main-picture')  # get all image tiles on the page
    total_count = len(images)

    for i in range(len(images)):  # loop in all images
        images = driver.find_elements(By.CLASS_NAME, 'main-picture')
        try:
            amazon_pr = amazon_price(images[i].get_attribute("src"))
        except:
            amazon_pr = 0.0
            pass
        amazon_pr = round(amazon_pr * exchange_rate_euro, 2)
        #print(amazon_pr)
        images[i].click()  #: click image to move to detail page
        sleep(20)

        driver.switch_to.window(driver.window_handles[-1])

        active_tab_text = driver.find_element(By.CLASS_NAME, 'od-pc-offer-tab-item-active').text

        drop_shipping = driver.find_elements(By.CLASS_NAME, 'od-pc-offer-tab-item')[1]
        # print(drop_shipping.text)
        cur_url = driver.current_url
        delivery_time = get_delivery_time(driver.find_elements(By.CLASS_NAME, 'logistics-text'))
        if(delivery_time != "48"):
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            continue
        if (drop_shipping.text == '代发'):
            drop_shipping.click()
        else:
            continue

        sleep(3)
        cur_url_b = driver.current_url

        # check if "重新登录(login again) dialog appears, if appear log in again to continue"
        # try:
        #     driver.find_element(By.CLASS_NAME,'next-dialog-btn').click()
        #     sleep(3)
        #     login(username,password)
        # except:
        #     pass

        if (True):
            if (driver.current_url != cur_url_b):
                driver.get(cur_url_b)
            batch = get_batch(driver.find_element(By.CLASS_NAME, 'unit-text').text)
            driver.get(cur_url)

            # print(delivery_time)
            if (batch == 1):
                full_title = translate_to_en(driver.find_element(By.CLASS_NAME, 'title-text').text)
                category_id = 0
                uncategorized_id = 0
                try:
                    for cat in categories:#get category id by checking full title involves category name or not
                        if('uncategorized' in cat['name'].lower().strip()):
                            uncategorized_id = cat['id']
                        if(cat['name'] in full_title):
                            category_id = cat['id']
                            break
                except:
                    pass
                if (cur_url != driver.current_url):
                    driver.get(cur_url)
                # print(cur_url)
                sleep(2)

                price = float(driver.find_element(By.CLASS_NAME, 'price-text').text)
                price = round(price * exchange_rate, 2)
                if amazon_pr < price and amazon_pr != 0.0:
                    print('skipped amazon price is less')
                    continue
                # get attribute name
                atr_name = translate_to_en(driver.find_element(By.CLASS_NAME, 'sku-prop-module-name').text)
                # scrolldown a bit to click expend triangle button
                driver.execute_script("window.scrollTo(0, 600);")
                try:
                    driver.find_element(By.CLASS_NAME, 'sku-wrapper-expend-button').click()
                    sleep(5)
                except:
                    pass
                if (cur_url != driver.current_url):
                    driver.get(cur_url)
                # get variations and attributes: convert formats to match API request data format

                sku_items = driver.find_elements(By.CLASS_NAME, 'sku-item-wrapper')
                variants = []
                attrs = [
                    {
                        "id": 0,
                        "name": atr_name,
                        "position": 0,
                        "visible": True,
                        "variation": True,
                        "options": variants
                    }
                ]
                attr_panel = driver.find_element(By.CLASS_NAME, 'offer-attr-list')

                attr_tags = attr_panel.find_elements(By.CLASS_NAME, 'offer-attr-item')
                i = 0
                for attr in attr_tags:
                    i += 1
                    atr_name = translate_to_en(attr.find_element(By.CLASS_NAME, 'offer-attr-item-name').text)
                    atr_value = attr.find_element(By.CLASS_NAME, 'offer-attr-item-value').text
                    attrs.append({
                        "id": i,
                        "name": atr_name,
                        "position": i,
                        "visible": True,
                        "variation": False,
                        "options": atr_value
                    })

                variations = []
                for item in sku_items:

                    variant_name = translate_to_en(item.find_element(By.CLASS_NAME, 'sku-item-name').text)
                    ################################
                    try:
                        variant_image = item.find_element(By.CLASS_NAME, 'sku-item-image')
                        style_attribute = variant_image.get_attribute('style')
                        # Extract the URL from the style attribute
                        url_start = style_attribute.find('url("') + len('url("')
                        url_end = style_attribute.find('")', url_start)
                        image_url = style_attribute[url_start:url_end]
                    except:
                        image_url=''
                    ################################

                    try:
                        variant_price = float(item.find_element(By.CLASS_NAME, 'discountPrice-price').text[
                                              :-1].strip()) * exchange_rate * 1.5  # uplift 0.5
                    except:
                        continue
                    variant_stock = get_batch(item.find_element(By.CLASS_NAME, 'sku-item-sale-num').text)

                    variants.append({'name': variant_name, 'price': variant_price, 'image': image_url})

                    variations.append({
                        'attributes': [
                            {
                                "id": variants.index(
                                    {'name': variant_name, 'price': variant_price, 'image': image_url}),
                                "option": variant_name
                            }
                        ],
                        "regular_price": str(round(variant_price, 2)),
                    })
                ##########################################
                colors = []
                try:
                    colors_elements = driver.find_elements(By.CLASS_NAME, 'prop-item')
                    for color in colors_elements:
                        colors.append(translate_to_en(color.text))

                except:
                    pass

                ############################################
                attrs[0]['options'] = variants
                # getting description
                description_panel = driver.find_elements(By.CLASS_NAME, 'layout-right')[1]
                # recheck "login again"
                # try:
                #     driver.find_element(By.CLASS_NAME,'next-dialog-btn').click()
                #     sleep(3)
                #     login(username,password)
                # except:
                #     pass
                element = driver.find_element(By.XPATH, '//div[contains(text(), "商品描述")]')
                element.click()
                # 跨境属性 Cross border properties
                try:
                    top_details = driver.find_element(By.CLASS_NAME, 'od-pc-offer-cross').text
                except:
                    top_details = ''
                # 商品属性 product properties
                try:
                    top_details_2 = driver.find_element(By.CLASS_NAME, 'od-pc-attribute').text
                except:
                    top_details_2 = ''

                top_details = translate_to_en(top_details + top_details_2)

                # move to bottom to load all descriptions and images

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(5)
                description_without_links = remove_external_links(driver.find_element(By.ID, 'detailContentContainer').get_attribute('innerHTML'))
                detail_description = translate_to_en(description_without_links
                    )
                # scrape product images
                images = driver.find_elements(By.CLASS_NAME, 'detail-gallery-img')
                image_srcs = ""
                for image in images:
                    image_srcs += image.get_attribute('src')
                    image_srcs += ","

                # check video exists
                try:

                    video_icon = driver.find_element(By.CLASS_NAME, 'video-icon')
                    video_icon.click()

                    video_link = driver.find_element(By.TAG_NAME, 'video').get_attribute('src')
                except:
                    video_link = ''

                video_html = ''
                # if video exists, add it top of description
                if (video_link != ''):
                    video_html = f'<p><video src="{video_link}" controls="" width="100%" height="496"></video></p>'

                detail_description = video_html + top_details + detail_description

                # extract reviews

                reviews_tab = driver.find_element(By.XPATH,
                                                  '//div[@class="next-tabs-tab-inner" and contains(text(), "买家评价")]')

                reviews_tab.click()

                sleep(1)

                reivews = []

                review_items = driver.find_elements(By.CLASS_NAME, 'evaluate-desc')

                for review_item in review_items:
                    reivews.append(translate_to_en(review_item.text))

                # JSON data for create product API request
                result = {
                    'name': full_title,
                    'regular_price': str(round(price* 1.5, 2)),  # uplift 0.5
                    'categories': [{'id': category_id}],
                    'sku': get_sku(driver.current_url),
                    'images': image_srcs,
                    'video': video_link,
                    'description': detail_description,
                    'additional_information': '',
                    'reviews': '\n\n'.join(reivews),
                    'attributes': attrs,
                    "type": "variable",
                    "colors": colors,

                }
                # create product via WooCommerce API : return product id
                # product_id = wc_import(result)
                # #add variations to created prodcut
                # variation_import(product_id,{"create":variations})
                #print(attrs)
                print(result)
                results.append(result)
                add_row(file_name, result)

        # close page
        driver.close()
        # return to supplier page
        driver.switch_to.window(driver.window_handles[-1])
    # move to next page
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), "下一页")]').click()
        sleep(10)
    except:
        break


# Assuming 'results' contains the scraped data in the desired format

# Define the file name and headers for the CSV file

print("Data has been exported to 'scraped_data.csv' file.")

print("Scraping Completed")
