import requests
from config import sites
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class Book():
    def __init__(self,ix=0):
        self.ix = ix
        self.site = sites[ix]

    def search_book(self,keyword):
        books = []
        if self.site == 'http://www.xbiquge.la':
            data = {"searchkey":keyword}
            url = self.site + '/modules/article/waps.php'
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
                    book['url'] = urlparse(tds[0].find('a')['href']).path 
                    book['last'] = tds[1].text.strip()
                    book['last_url'] = tds[1].find('a')['href']
                    book['author'] = tds[2].text.strip()
                    book['last_update_time'] = tds[3].text.strip()
                    books.append(book)
        if self.site == 'https://www.biquge.lol':
            url = self.site + '/ar.php?keyWord=' + keyword
            res = requests.get(url)
            res.encoding = "utf-8"
            soup = BeautifulSoup(res.text, 'lxml')
            container = soup.find('div',class_='container')
            ul = container.find('ul')
            lis = ul.find_all('li')[1:]
            for li in lis:
                book = {'name':'','author':'','last':'','last_update_time':'','url':'','last_url':''}
                book['name'] = li.find('span',class_="s2").find('a').text
                book['url'] = li.find('span',class_="s2").find('a')['href']
                book['last'] = li.find('span',class_="s3").find('a').text
                book['last_url'] = li.find('span',class_="s3").find('a')['href']
                book['author'] = li.find('span',class_="s4").text
                book['last_update_time'] = li.find('span',class_="s5").text
                books.append(book)
        return books

    def get_chapters(self,path):
        book = {'name':'','author':'','url':'','desc':'','chapters':[]}
        url = self.site + path
        if self.site == 'http://www.xbiquge.la':
            res = requests.get(url)
            res.encoding = "utf-8"
            soup = BeautifulSoup(res.text, 'lxml')
            maininfo = soup.find('div',id='maininfo')
            book['name'] = maininfo.find('div',id='info').find('h1').text
            book['url'] = path
            book['author'] = maininfo.find('div',id='info').find('p').text.split("：")[1].strip()
            book['desc'] = maininfo.find('div',id='intro').find_all('p')[1].text
            wrapper = soup.find('div',id='wrapper')
            dl_dds = wrapper.find('div',id='list').find('dl').find_all('dd')
            for dd in dl_dds:
                chapter = {'name':'','url':''}
                chapter['name'] = dd.find('a').text
                chapter['url'] = dd.find('a')['href']
                book['chapters'].append(chapter)
        if self.site == 'https://www.biquge.lol':
            
        return book

    def get_chapter(self,path):
        chapter = {'url':path,'name':'','pre_url':'','next_url':'','chapters_url':'','context':''}
        url = self.site + path
        if self.site == 'http://www.xbiquge.la':
            res = requests.get(url)
            res.encoding = "utf-8"
            soup = BeautifulSoup(res.text, 'lxml')
            box_con = soup.find('div',id='wrapper').find('div',class_='content_read').find('div',class_='box_con')
            info = box_con.find('div',class_='bookname')
            chapter['name'] = info.find('h1').text
            cinfo = info.find('div',class_='bottem1')
            chapter['pre_url'] = cinfo.find('a',text='上一章')['href']
            chapter['next_url'] = cinfo.find('a',text='下一章')['href']
            chapter['chapters_url'] = urlparse(cinfo.find('a',text='章节目录')['href']).path
            chapter['context'] = box_con.find('div',id='content').text
        return chapter







def main():
    book = Book(1)
    book.search_book("大主宰")
    # book.get_chapters('/0/8/')
    # book.get_chapter('/0/8/7011294.html')



if __name__ == '__main__':
    main()





