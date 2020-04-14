from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as urlReq
import re

url = 'https://earthview.withgoogle.com'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
try:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    image_urls = set()
    countries = set()
    num_unknown = 1
    with open('images_urls.txt','w') as file:
        import sys
        if len(sys.argv) == 2:
            num_images = sys.argv[1]
        else:
            num_images = 10
        for i in range(int(num_images)): #get input for number of images at least

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
            country_name = page_soup.find_all('div', {'class':'location__country'})

            for image in images:
                curr_url = image['src']
                image_urls.add(curr_url)
            
            if country_name[0].next != '':
                countries.add(country_name[0].next)
            else:
                countries.add('Uknown_image' + str(num_unknown))
                num_unknown += 1
            
        print(countries)

        for country,url in zip(countries,image_urls):
            file.write(country + '\n')
            file.write(url + '\n')

    driver.close()

    import os
    os.system('python3 download_images.py')
except:
    driver.close()
    print("error")


