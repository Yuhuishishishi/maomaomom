# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup
import re
import recipe
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


href = hrefs[6]

r = recipe.get_recipe_from_web(href)
    
os.mkdir('./'+r.title)
f = open('./'+r.title + '/' + 'instructions.txt', 'w')
for step in r.instructions:
    f.write(step.encode('utf-8'))
    f.write('\n')
    
f.close()


