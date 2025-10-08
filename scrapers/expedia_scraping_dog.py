from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Use Playwright's ChromeDriver if available
import os
playwright_chrome_path = '/Users/oco/Library/Caches/ms-playwright/chromium-1187/chrome-mac/Chromium.app/Contents/MacOS/Chromium'
l=list()
o={}

options = webdriver.ChromeOptions()

options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36')
options.add_argument('accept-encoding=gzip, deflate, br')
options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
options.add_argument('referer=https://www.expedia.com/')
options.add_argument('upgrade-insecure-requests=1')

target_url='https://www.expedia.com/Cansaulim-Hotels-Heritage-Village-Resort-Spa-Goa.h2185154.Hotel-Information?=one-key-onboarding-dialog&chkin=2023-05-13&chkout=2023-05-14&destType=MARKET&destination=Goa%2C%20India%20%28GOI-Dabolim%29&latLong=15.383019%2C73.838253&regionId=6028089&rm1=a2'
# Set up ChromeDriver with Playwright's Chrome if available
if os.path.exists(playwright_chrome_path):
    options.binary_location = playwright_chrome_path
    driver = webdriver.Chrome(options=options)
else:
    # Fallback to system Chrome
    driver = webdriver.Chrome(options=options)
driver.get(target_url)
time.sleep(5000)
resp=driver.page_source
driver.close()
print(resp)


