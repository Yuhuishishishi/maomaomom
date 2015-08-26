# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 19:50:58 2015

@author: yuhuishi
"""

import requests
from bs4 import BeautifulSoup
import re

class Recipe:
    
    def __init__(self, title, instructions, imgs):
        self.title = title;
        self.instructions = instructions
        self.imgs = imgs
        

def get_recipe_from_web(href):
    # get the response
    res = requests.get(href.strip())
    html = res.text
    
    #%% parse the page
    page = BeautifulSoup(html)
    div_content = page.find('div', class_='entry-content')    
    
    # title
    title_tag = div_content.find('span', style='color: #008000;')
    title = title_tag.string
    
    # the instruction list
    pattern = re.compile(ur'\d[：|、].*[；|。]', re.U)
    matches = pattern.findall(unicode(div_content))
    
    # the images
    img_recipe_list = []
    imgs = div_content.find_all('img')
    for img in imgs:
        src = img['src']
        if re.compile('http://maomaomom').search(src):
            img_recipe_list.append(src)
            
    r = Recipe(title, matches, img_recipe_list)
    return r
        
        