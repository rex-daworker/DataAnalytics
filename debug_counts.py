import os, re
from bs4 import BeautifulSoup

BASE='/Users/rexoghenerobo/Downloads/Datasets'
path=os.path.join(BASE,'macworld')
folders=[f for f in os.listdir(path) if os.path.isdir(os.path.join(path,f))][:5]
for folder_name in folders:
    folder=os.path.join(path,folder_name)
    html=os.path.join(folder,'index.html')
    tags=os.path.join(folder,'tags.txt')
    print('->',folder_name)
    with open(tags,'r',encoding='utf-8',errors='ignore') as f:
        content=f.read().strip()
    print('  tags content:', repr(content[:80]))
    keywords=[k.strip() for k in content.split(',')] if ',' in content else content.split('\n')
    print('  keywords count',len(keywords),keywords[:5])
    with open(html,'r',encoding='utf-8',errors='ignore') as f:
        htmltext=f.read()
    soup=BeautifulSoup(htmltext,'html.parser')
    text=' '.join(t.get_text() for t in soup.find_all('p'))
    def clean_text(t):
        t=t.lower()
        t=re.sub(r'[^a-z0-9\s]',' ',t)
        return ' '.join(t.split())
    def count(text, kws):
        if not text or not kws: return 0
        ct=clean_text(text)
        tot=0
        for kw in kws:
            tot+=len(re.findall(r'\b'+re.escape(clean_text(kw))+r'\b',ct))
        return tot
    print('  p count',count(text,keywords))
