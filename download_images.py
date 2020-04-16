import pandas as pd 
import urllib.request as req
import os
import os.path
from os import path
import shutil


images_folder = 'images/'

if path.exists(images_folder): #remove all images in folder by deleting folder
    shutil.rmtree(images_folder)


os.mkdir(images_folder) #remake folder for images
    
with open('images_urls.txt','r') as file:
    urls = file.readlines()

it = iter(urls)
for pair in it:
    country = pair.replace(' ','_')
    filename = country.replace('\n','') + '.jpg'
    full_path = '{}{}'.format(images_folder,filename)
    url = next(it).replace('\n','')
    req.urlretrieve(url,full_path)






