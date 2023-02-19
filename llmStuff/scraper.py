from urllib.request import urlopen
from bs4 import BeautifulSoup

def replaceNewLines(text):
    return text.replace('\n', ' ').replace('\r', '')

quote_page = "https://upakka.com/www.upakka.com/index.html"
page = urlopen(quote_page)
soup = BeautifulSoup(page)
txt = replaceNewLines(soup.get_text())
with open("output.txt", "w") as f:
    for token in txt:
        try:
            f.write(token)
        except:
            pass