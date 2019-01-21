# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup

with open('./luckyday_page.html') as fr:
    text = fr.read()

bs = BeautifulSoup(text, "lxml")
posts = bs.find_all('div', {'role': 'article'})
for p in posts:
    like = p.find('a', {'class': 'ex ey'})
    span = like.find('span')
    print like.text
    print like['href']


