import pandas as pd 
import urllib.request as req
import os
from os import path
from os import listdir
import shutil
import argparse
import glob



def parse_arguments():
    parser = argparse.ArgumentParser()


    # Optional argument for foldername
    parser.add_argument('--folder', type=str, default = None,
                        help='A required integer positional argument')

    args = parser.parse_args()

    

    folder_name = args.folder

    return folder_name


images_folder = 'images/'

folder_name = parse_arguments()


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

if folder_name is not None:

    if path.exists(folder_name): #remove all images in folder by deleting folder

        imgs = os.listdir(folder_name)
        for img in imgs:
            #source, destination
            #copy from from folder_name to images_folder
            shutil.copy(os.path.join(folder_name,img), images_folder)




