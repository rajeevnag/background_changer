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

file_number = 0
for url in urls:
    filename = 'earth_image_' + str(file_number) + '.jpg'
    full_path = '{}{}'.format(images_folder,filename)
    req.urlretrieve(url,full_path)
    file_number += 1







