from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import argparse
import time
import os
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as urlReq
import re
import sys



url = 'https://earthview.withgoogle.com'



def parse_arguments():
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument('--num_images', type=int, default=50,
                        help='A required integer positional argument')

    # Optional argument for foldername
    parser.add_argument('--folder', type=str, default = None,
                        help='A required integer positional argument')

    args = parser.parse_args()

    num_images = args.num_images
    
    folder_name = args.folder

    return num_images, folder_name





try:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    image_urls = set()
    countries = list()
    duplicate_countries = {}

    num_images, folder_name = parse_arguments()

    with open('images_urls.txt','w') as file:

        last_country = str()
        driver.get(url)
        
        button = driver.find_element_by_class_name('intro__explore')
        button.click()
        while len(image_urls) != num_images: #get input for number of images at least
            time.sleep(.2)
            
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
                        curr_name = str()
                        
                        try:
                            curr_name += country_name[0].previous
                            curr_name +='-'
                            curr_name += country_name[0].next
                        except:
                            curr_name = str()
                            curr_name += "unknown"
                            curr_name +='-'
                            curr_name += country_name[0].next

                        if curr_name in duplicate_countries: #check if seen before
                            duplicate_countries[curr_name] += 1
                            file.write(curr_name)
                            file.write(str(duplicate_countries[curr_name]) + '\n')
                        else:
                            duplicate_countries[curr_name] = 1
                            file.write(curr_name + '\n')

                        file.write(curr_url + '\n')

                driver.find_element_by_tag_name('body').send_keys(Keys.RIGHT)
            except:
                pass


    driver.close()
    
    optional_folder_name = f" --folder {folder_name}"
    command = "python3 download_images.py"
    
    if folder_name is not None:
        command = command + optional_folder_name

    print(command)
    os.system(command)
except:
    driver.close()








