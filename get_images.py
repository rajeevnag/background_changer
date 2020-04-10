from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as urlReq
import re

url = 'https://earthview.withgoogle.com'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
image_urls = set()

with open('images_urls.txt','w') as file:
    import sys
    x = sys.argv[1]
    for i in range(int(sys.argv[1])): #get input for number of images at least

        driver.implicitly_wait(30)
        driver.get(url)
        menu = driver.find_element_by_class_name('main')
        actions = ActionChains(driver)
        actions.double_click(menu)
        url = driver.current_url

        uClient = urlReq(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        images = page_soup.find_all('img', {'src':re.compile('.jpg')})

        for image in images:
            curr_url = image['src']
            image_urls.add(curr_url)

    for url in image_urls:
        file.write(url + '\n')

driver.close()

import os
os.system('python3 download_images.py')
