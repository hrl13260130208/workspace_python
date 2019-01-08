



import spider_c.spider_modules.job as job
import spider_c.spider_modules.name_manager as nm
import spider_c.spider_modules.standard_spider_back as ss
import re
from bs4 import BeautifulSoup
import requests
import math
import time
import random


def get_html(url):
    data = requests.get(url)
    data.encoding = 'utf-8'
    datatext = data.text
    data.close()
    time.sleep(5 * random.random())
    return datatext



class first(ss.ThreadingSpider):

    def get(self,url):
        url = "http://www.freepatentsonline.com/featured/patentclasses.html"
        urls=[]
        html = get_html(url)

        soup = BeautifulSoup(html, "html.parser")
        table_tag = soup.find("table", class_="listing_table")
        for a_tag in table_tag.find_all("a"):
            urls.append("http://www.freepatentsonline.com" + a_tag["href"])

        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
        html = get_html(url)
        urls = []
        soup = BeautifulSoup(html, "html.parser")
        table_tag = soup.find("div", class_="well well-small")
        td = table_tag.find("td", width="36%")
        tstr = td.get_text()
        num = re.search("of", tstr).span()
        print(tstr[num[1]:])

        s = math.ceil(int(tstr[num[1]:]) / 50)
        if s > 200:
            s = 200
        s = s - 1

        urls.append("http://www.freepatentsonline.com/CCL-367.html")
        for i in range(s):
            urls.append("http://www.freepatentsonline.com/CCL-367-p" + str(i + 2) + ".html")
        return urls

class thrid(ss.ThreadingSpider):
    def get(self,url):
        html = get_html(url)
        urls = []
        soup = BeautifulSoup(html, "html.parser")
        div_tag = soup.find("div", class_="container_white")
        for a_tag in div_tag.find_all("a"):
            urls.append("http://www.freepatentsonline.com" + a_tag["href"])

        return urls
class four(ss.ThreadingSpider):
    def get(self,url):
        html = get_html(url)
        text = ""
        soup = BeautifulSoup(html, "html.parser")
        for div in soup.find_all("div", class_="disp_doc2"):

            if div.find("div", class_="disp_elm_title"):
                dtitle = div.find("div", class_="disp_elm_title").get_text()
                if dtitle:
                    line = div.get_text().strip().replace("\n", "")
                    text = text + line + "$$$$"

        self.file.write(url+"$$$$"+text[:-4]+"\n")


if __name__ == '__main__':
    file_path = "C:/file/ResultFile/fpo_spider_result.txt"
    f = open(file_path, "a+",encoding="utf-8")
    names = nm.Name_Manager("fpo", 4)
    j = job.Job(f)


    fi=first(names)
    se=second(names)
    th=thrid(names)
    fo=four(names)
    j.start(names, fi,se,th,fo)




