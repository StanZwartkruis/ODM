import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException
import sys
import ssl
import csv

# Define a custom Scrapy spider for scraping keyboard information from thomann.de
class KeyboardSpider(scrapy.Spider):
    # Name of the spider, used for running it
    name = 'keyboardspider'
    # Restrict the spider to a specific domain
    allowed_domains = ['thomann.de']
    # URLs where the spider begins crawling
    start_urls = ['https://www.thomann.de/nl/home_keyboards.html']

    # Custom settings for the spider
    custom_settings = {
        'ROBOTSTXT_OBEY': True,  # Respect the robots.txt file
        'AUTOTHROTTLE_ENABLED': True,  # Enable dynamic download delay
        'AUTOTHROTTLE_START_DELAY': 5,  # Initial delay before start (in seconds)
        'DOWNLOAD_DELAY': 2,  # Delay between requests (in seconds)
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # Maximum concurrent requests per domain
    }

    # Initialize the spider
    def __init__(self, *args, **kwargs):
        chrome_options = Options()
        # Uncomment to run Chrome in headless mode (no browser UI)
        chrome_options.add_argument("--headless")

        # Setup proxy settings for the browser
        proxy_url = "127.0.0.1:24000"
        chrome_options.add_argument(f'--proxy-server={proxy_url}')
        # Set a custom user-agent for the browser
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"')
        # Ignore SSL and certificate errors
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')

        # Define the path to the ChromeDriver
        chrome_url = r'/path/to/chromedriver'
        chrome_service = Service(chrome_url)
        # Initialize Selenium WebDriver with Chrome
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

self.csv_file = open("products.csv", "w", newline="", encoding="utf-8")
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=[
            "product_name", "product_brand"
        ])
        self.csv_writer.writeheader()

    # Method to parse the response and extract data
    def parse(self, response):
        # Loop through each product item and extract details
        for product in response.css('div.product'):
            scraped_data = {
                'product_name': product.css('span.title_name::text').get(default='').strip(),
                #'product_price': product.css('div.price-price::text').get(),
                'product_brand': product.css('span.title_manufacturer::text').get(),
                #'number_of_reviews': product.css('span.reviews-count::text').get(),
                #'product_url': response.urljoin(product.css('a::attr(href)').get()),
                #'stock_availability': product.css('div.stock-status::text').get().strip() if product.css('div.stock-status::text').get() else None,
            }

    self.csv_writer.writerow(scraped_data)

    yield scraped_data

        # Handle pagination by following the next page link
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            # Make a request to the next page and continue parsing
            yield scrapy.Request(next_page_url, callback=self.parse)

# Proxy setup
if sys.version_info[0] == 2:
    import six
    from six.moves.urllib import request
elif sys.version_info[0] == 3:
    import urllib.request

    def setup_proxy():        
        ctx = ssl.create_default_context()
        ctx.verify_flags = ssl.VERIFY_DEFAULT

        if sys.version_info[0] == 2:
            opener = request.build_opener(
                request.ProxyHandler({'http': 'http://127.0.0.1:24000'}),
                request.HTTPSHandler(context=ctx)
            )
        elif sys.version_info[0] == 3:
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler({'http': 'http://127.0.0.1:24000'}),
                urllib.request.HTTPSHandler(context=ctx)
            )
    
    setup_proxy()
    
    from w3lib.http import basic_auth_header

    class CustomProxyMiddleware(object):
        def process_request(self, request, spider):
            request.meta['proxy'] = "http://127.0.0.1:24000"
    
    # Conditional import and setup for proxy support based on Python version
if sys.version_info[0] == 2:
    # Python 2 specific imports
    import six
    from six.moves.urllib import request
elif sys.version_info[0] == 3:
    # Python 3 specific import
    import urllib.request

    # Function to setup a proxy server
    def setup_proxy():        
        # Create a default SSL context for handling HTTPS requests
        ctx = ssl.create_default_context()
        # Set default verification flags for SSL
        ctx.verify_flags = ssl.VERIFY_DEFAULT

        # For Python 2, configure an opener with proxy settings
        if sys.version_info[0] == 2:
            opener = request.build_opener(
                request.ProxyHandler({'http': 'http://127.0.0.1:24000'}),  # Set up HTTP proxy
                request.HTTPSHandler(context=ctx)  # Add handler for HTTPS with SSL context
            )
        # For Python 3, configure an opener with proxy settings
        elif sys.version_info[0] == 3:
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler({'http': 'http://127.0.0.1:24000'}),  # Set up HTTP proxy
                urllib.request.HTTPSHandler(context=ctx)  # Add handler for HTTPS with SSL context
            )
    
    # Execute the proxy setup function
    setup_proxy()
    
    # Import basic authentication header utility
    from w3lib.http import basic_auth_header

    # Custom middleware class for Scrapy
    class CustomProxyMiddleware(object):
        # Method to process each request made by the Scrapy spider
        def process_request(self, request, spider):
            # Set up the proxy for the request using meta attribute
            request.meta['proxy'] = "http://127.0.0.1:24000"

