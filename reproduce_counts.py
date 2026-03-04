import os, re
from bs4 import BeautifulSoup

BASE='/Users/rexoghenerobo/Downloads/Datasets'
folder='article--2980650--smartphones--saving-private-apple-a-solution-in-search-of-a-problem.html'
path=os.path.join(BASE,'macworld',folder)
html_path=os.path.join(path,'index.html')
tags_path=os.path.join(path,'tags.txt')

with open(tags_path,'r',encoding='utf-8',errors='ignore') as f:
    content=f.read().strip()
    print('raw tags content:',content[:200])
    keywords=[k.strip() for k in content.split(',')] if ',' in content else content.split('\n')
    print('keywords',keywords)

with open(html_path,'r',encoding='utf-8',errors='ignore') as f:
    soup=BeautifulSoup(f.read(),'html.parser')

# functions

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = ' '.join(text.split())
    return text

def count_keywords(text, keywords):
    if not text or not keywords:
        return 0
    clean = clean_text(text)
    total = 0
    for kw in keywords:
        kw_clean = clean_text(kw)
        pattern = r'\b' + re.escape(kw_clean) + r'\b'
        hits = len(re.findall(pattern, clean))
        if hits:
            print('found',hits,'for',kw_clean)
        total += hits
    return total

text = ' '.join(tag.get_text() for tag in soup.find_all('p'))
print('p total',count_keywords(text, keywords))
a_text = ' '.join(tag.get_text() for tag in soup.find_all('a'))
print('a total',count_keywords(a_text, keywords))
