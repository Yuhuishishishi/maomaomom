# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup
import re
from recipe import Recipe
import os

# open the base page

url = 'http://maomaomom.com/zh/%E4%B8%AD%E5%BC%8F%E7%94%9C%E7%82%B9%E5%88%86%E7%B1%BB/'
res = requests.get(url)

html = res.text
page = BeautifulSoup(html)

print page.prettify()

#%% parse the page


container = page.find('div', class_='entry-content')

def in_maomaoma_web(href):
    return href.startswith(' http://maomaomom.com') or href.startswith('http://maomaomom.com')
    
def has_img_child(tag):
    if len(tag.contents) == 0:
        return False
    try:
        child = tag.contents[0].name
    except AttributeError:
        return False
    if child == None:
        return False
    if re.compile('img').search(child):
        return True
    else:
        return False
    
links = container.find_all(has_img_child, href=in_maomaoma_web)

hrefs = []
imgsrcs = []
for link in links:
    href = link['href']
    img = link.contents[0]
    src = img['src']
    
    hrefs.append(href)
    imgsrcs.append(src)
    
    print href, src
    
#%% redirect to detailed recipe


href = hrefs[1]

res = requests.get(href.strip())
html = res.text

#%% parse the page
page = BeautifulSoup(html)
div_content = page.find('div', class_='entry-content')    

# title
title_tag = div_content.find('span', style='color: #008000;')
title = title_tag.string

# the instruction list
pattern = re.compile('\d[：|、].*[；|。]', re.U)
matches = pattern.findall(str(div_content))

# the images
img_recipe_list = []
imgs = div_content.find_all('img')
for img in imgs:
    src = img['src']
    if re.compile('http://maomaomom').search(src):
        img_recipe_list.append(src)
    

r = Recipe(title, matches, img_recipe_list)
    
os.mkdir('./'+r.title)
f = open('./'+r.title + '/' + 'instructions.txt', 'w')
for step in r.instructions:
    f.write(step)
    f.write('\n')
    
f.close()


