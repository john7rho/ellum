from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm

def replaceNewLines(text):
    return text.replace('\n', ' ').replace('\r', '')

quote_page = "https://www.ketnipz.com/collections/shop-all"
page = urlopen(quote_page)
soup = BeautifulSoup(page) 
txt = replaceNewLines(soup.get_text())
with open("output.txt", "w") as f:
    for idx in tqdm(range(len(txt))):
        token = txt[idx]
        try:
            f.write(token)
        except:
            pass