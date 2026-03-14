from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import re, pathlib
p = pathlib.Path('index_en.html')
html = p.read_text(encoding='utf-8')
soup = BeautifulSoup(html, 'html.parser')

# gather unique arabic texts in nodes and attributes
texts = set()
for t in soup.find_all(text=True):
    s = t.string
    if s and re.search('[\u0600-\u06FF]', s):
        stripped = s.strip()
        if stripped:
            texts.add(stripped)

attrs = ['placeholder', 'alt', 'title', 'aria-label']
for el in soup.find_all(True):
    for attr in attrs:
        if el.has_attr(attr):
            v = el[attr].strip()
            if v and re.search('[\u0600-\u06FF]', v):
                texts.add(v)

print('Arabic text count:', len(texts))
texts = sorted(texts, key=lambda x:(-len(x), x))
translator = GoogleTranslator(source='ar', target='en')
translation_map = {}
# Avoid repeated calls for very similar ones
for t in texts:
    try:
        # skip if already English enough
        if re.search('[a-zA-Z]', t) and not re.search('[\u0600-\u06FF]', t):
            continue
        translated = translator.translate(t)
        translation_map[t] = translated
        print('> %s -> %s' % (t, translated))
    except Exception as e:
        print('ERR:', t, e)

# Apply translation
for t_node in soup.find_all(text=True):
    s = t_node.string
    if s and t_node.string.strip() in translation_map:
        new = t_node.string.replace(t_node.string.strip(), translation_map[t_node.string.strip()])
        t_node.replace_with(new)

for el in soup.find_all(True):
    for attr in attrs:
        if el.has_attr(attr):
            val = el[attr].strip()
            if val in translation_map:
                el[attr] = translation_map[val]

p.write_text(str(soup), encoding='utf-8')
print('Done')
