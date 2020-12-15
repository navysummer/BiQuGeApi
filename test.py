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
            res.encoding = "utf-8"
            soup = BeautifulSoup(res.text, 'lxml')
            table = soup.find('table')
            trs = table.find_all('tr')
            books = []
            for tr in trs:
                tds = tr.find_all('td')
                book = {'name':'','author':'','last':'','last_update_time':'','url':'','last_url':''}
                if tds:
                    book['name'] = tds[0].text.strip()
                    book['url'] = tds[0].find('a')['href']
                    book['last'] = tds[1].text.strip()
                    book['last_url'] = self.site + tds[1].find('a')['href']
                    book['author'] = tds[2].text.strip()
                    book['last_update_time'] = tds[3].text.strip()
                    books.append(book)
            return books



def main():
    book = Book()
    book.search_book("大主宰")



if __name__ == '__main__':
    main()





