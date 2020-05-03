from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as urlReq
import re

url = 'https://earthview.withgoogle.com'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
try:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    image_urls = set()
    countries = list()
    duplicate_countries = {}
    with open('images_urls.txt','w') as file:
        import sys
        if len(sys.argv) == 2:
            num_images = sys.argv[1]
        else:
            num_images = 50

        last_country = str()
        while len(image_urls) != int(num_images): #get input for number of images at least
            driver.implicitly_wait(30)
            time.sleep(2)
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
            country_name = page_soup.find_all('div', {'class':'location__country'})
            try:
                for image in images:
                    curr_url = image['src']
                    if curr_url not in image_urls: #new image
                        image_urls.add(curr_url)
                        
                        if country_name[0].next in duplicate_countries:
                            duplicate_countries[country_name[0].next] += 1
                            file.write(country_name[0].next)
                            file.write(str(duplicate_countries[country_name[0].next]) + '\n')
                        else:
                            duplicate_countries[country_name[0].next] = 1
                            file.write(country_name[0].next + '\n')

                        file.write(curr_url + '\n')
            except:
                pass


    driver.close()

    import os
    os.system('python3 download_images.py')
except:
    driver.close()
    breakpoint()
    print("error")


