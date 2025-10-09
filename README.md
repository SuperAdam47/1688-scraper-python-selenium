1688 Scraper + WooCommerce Uploader v1.0
It's console based script so all actions must be done in cmd/git bash/powershell
# Project based
    - Python Selenium for extraction
    - WooCommerce REST API

# Requirements
    - Install required python libraries on virtualenv
        virtualenv venv
        source venv/bin/activate (MacOS, Linux OS)
        venv\scripts\activate(Windows OS)
        pip install -r requirements.txt
    - Place corresponding chromedriver.exe in the directory.
    ** Cause chromedriver is not automatically downloaded after version 114, you need to place the one matching your current web browser version in the project directory.
    ** The given chromedriver is version 119

# How to run the script.
    - Activate virtualenv
        source venv/bin/activate (MacOS, Linux OS)
        venv\scripts\activate(Windows OS)
    - Run the file
        Python scraper.py
    - Input supplier URL and press Enter


v1.0 Developer : aarontapi3@gmail.com
