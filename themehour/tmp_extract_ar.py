from bs4 import BeautifulSoup
import re, pathlib
p = pathlib.Path('index_en.html')
html = p.read_text(encoding='utf-8')
soup = BeautifulSoup(html, 'html.parser')
texts=set()
for t in soup.find_all(text=True):
    s=t.strip()
    if not s: continue
    if re.search('[\u0600-\u06FF]', s):
        texts.add(s)
for el in soup.find_all(True):
    for attr in ['placeholder','alt','title','aria-label']:
        if el.has_attr(attr):
            v = el[attr].strip()
            if v and re.search('[\u0600-\u06FF]', v):
                texts.add(v)
for t in sorted(texts, key=lambda x:(-len(x), x)):
    print(repr(t))
print('TOTAL', len(texts))
