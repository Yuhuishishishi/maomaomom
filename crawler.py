# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup
import re

# open the base page

url = 'http://maomaomom.com/zh/%E4%B8%AD%E5%BC%8F%E7%94%9C%E7%82%B9%E5%88%86%E7%B1%BB/'
res = requests.get(url)

html = res.text
page = BeautifulSoup(html)

print page.prettify()

#%% parse the page


container = page.find('div', class_='entry-content')

def in_maomaoma_web(href):
    return href.startswith(' http://maomaomom.com')
        or href.startswith('http://maomaomom.com')
    
def has_img_child(tag):
    if len(tag.contents) == 0:
        return False
    child = tag.contents[0].name
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


href = hrefs[0]

res = requests.get(href.strip())
html = res.text

#%% parse the page
page = BeautifulSoup(html)
div_content = page.find('div', class_='entry-content')    

stepre = re.compile('^\d.*')
pp = stepre.search(str(div_content))


