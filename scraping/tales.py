from lxml import etree
import lxml.html
import requests

def parse(url):
    data = requests.get(url)
    tree = lxml.html.document_fromstring(data.text)
    link = tree.xpath()
    

def main():
    url = "https://deti-online.com/audioskazki/"
    parse(url)

if __name__ == "__main__":
    main()