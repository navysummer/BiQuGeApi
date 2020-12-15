import requests
from config import sitesConfig,sites
from bs4 import BeautifulSoup

class Book():
    def __init__(self,ix=0):
        self.ix = ix
        self.site = sites[ix]
        self.siteConfig = sitesConfig[self.site]

    def search_book(self,keyword):
        books = []
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

    def get_chapters(self,url):
        book = {'name':'','author':'','url':'','desc':'','chapters':[]}
        if url.find('www.xbiquge.la') != -1:
            res = requests.get(url)
            res.encoding = "utf-8"
            soup = BeautifulSoup(res.text, 'lxml')
            maininfo = soup.find('div',id='maininfo')
            book['name'] = maininfo.find('div',id='info').find('h1').text
            book['url'] = url
            book['author'] = maininfo.find('div',id='info').find('p').text.split("：")[1].strip()
            book['desc'] = maininfo.find('div',id='intro').find_all('p')[1].text
            wrapper = soup.find('div',id='wrapper')
            dl_dds = wrapper.find('div',id='list').find('dl').find_all('dd')
            for dd in dl_dds:
                chapter = {'name':'','url':''}
                chapter['name'] = dd.find('a').text
                chapter['url'] = self.site + dd.find('a')['href']
                book['chapters'].append(chapter)
        return book

    def get_chapter(self,url):
        chapter = {'url':url,'name':'','pre_url':'','next_url':'','chapters_url':'','context':''}
        if url.find('www.xbiquge.la') != -1:
            res = requests.get(url)
            res.encoding = "utf-8"
            soup = BeautifulSoup(res.text, 'lxml')
            box_con = soup.find('div',id='wrapper').find('div',class_='content_read').find('div',class_='box_con')
            info = box_con.find('div',class_='bookname')
            chapter['name'] = info.find('h1').text
            cinfo = info.find('div',class_='bottem1')
            chapter['pre_url'] = self.site + cinfo.find('a',text='上一章')['href']
            chapter['next_url'] = self.site + cinfo.find('a',text='下一章')['href']
            chapter['chapters_url'] = self.site + cinfo.find('a',text='章节目录')['href']
            chapter['context'] = box_con.find('div',id='content').text
        print(chapter)
        return chapter







def main():
    book = Book()
    # book.search_book("大主宰")
    # book.get_chapters('http://www.xbiquge.la/0/8/')
    book.get_chapter('http://www.xbiquge.la/0/8/7011294.html')



if __name__ == '__main__':
    main()





