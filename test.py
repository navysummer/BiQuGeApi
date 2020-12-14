from lxml import etree
import requests
from config import sitesConfig,sites
from bs4 import BeautifulSoup

class Book():
    def __init__(self,ix=0):
        self.ix = ix
        self.site = sites[ix]
        self.siteConfig = sitesConfig[self.site]

    def search_book(self,keyword):
        method = self.siteConfig['search']['method']
        if method == 'POST':
            if self.site == 'http://www.xbiquge.la':
                data = {"searchkey":keyword}
            url = self.site + self.siteConfig['search']['path']
            res = requests.post(url,data=data)
            # soup = BeautifulSoup(res.text.encode("ISO-8859-1").decode("utf-8"), 'lxml')
            # table = soup.find('table')
            # print(table)
            # print(res.encoding)
            res.encoding = "utf-8"
            # print(res.text)
            tree = etree.HTML(res.text)
            # print(tree)
            xp = self.siteConfig['search']['xpath']
            # print(xp.extract())
            rt = tree.xpath(xp)
            # print(rt)
            for item in rt:
                content = etree.tostring(item, method='html')
                
                print(content)



def main():
    book = Book()
    book.search_book("大主宰")



if __name__ == '__main__':
    main()





