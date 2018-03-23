#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import random

img_ext = ['jpg','png','peg','img']

directory = sys.argv[1]

try:
    dir_list = os.scandir(directory)
except:
    print("no such directory")
    sys.exit('no such directory')

def select_subdir():
    subdir_list = []
    #print('dir_list inside function' + str(dir_list))
    for every in dir_list:
        #print(every.name)
        if every.is_dir():
            subdir_list.append(every.name)
    #print('subdir list ' + str(subdir_list))
    random_subdir = random.choice(subdir_list)
    return random_subdir

def image_founder(random_subdir):
    subdir_files = os.scandir(directory + "/" + random_subdir)
    files_list = []
    for every in subdir_files:
        if every.is_file():
            if every.name[-3:].lower() in img_ext:
                files_list.append(every.name)
            else:
                pass
                #print(every.name + ' not image')
    try:
        random_image = random.choice(files_list)
        print(random_image)
        return random_image
    except:
        print('No images found in this directory')

check_name = 'r0mk'

dir_list = (os.scandir(directory))
while True:
    dir_list = os.scandir(directory)
    random_dir = select_subdir()
    print('Random dir is ' + random_dir)
    if image_founder(random_dir):
        print('Hoooray')
        break 
    else:
        print('trying next subdir\n')
        
else:
    print('continue')


#if files_list == []:
#    print('no files')

#print(files_list)

#random_image = random.choice(files_list)

#def select_rand_image()
#    random_image = random.choice(files_list)
#    if random_image[:-3] not in ['jpg','JPG']
#        then
    
#print(random.choice(os.listdir(directory)))

#print()
#print(os.listdir(directory))
#print(random.uniform(1, 10))


