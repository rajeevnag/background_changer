from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as urlReq
import re


url = 'https://earthview.withgoogle.com'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install())

with open('images.txt','w') as file:
    for i in range(10):

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
            file.write(image['src'] + '\n')




