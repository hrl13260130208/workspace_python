from concurrent.futures import  ThreadPoolExecutor,as_completed,Future
import requests
from bs4 import  BeautifulSoup
import spider.spider_modules.standard_spider as ss
import spider.spider_modules.name_manager as nm
import spider.spider_modules.job as job
import re
import time



def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.ThreadingSpider):

    def get(self,url):
        print("111111111")
        urls = []
        url = "http://soeasycenter.com/newTender"

        parm = {
            "periodTime": " 0.0",
            "pageNum": "1",
            "pageSize": "500",
        }

        data = requests.post(url, data=parm)
        data.encoding = "utf-8"
        data = data.text

        soup = BeautifulSoup(data, "html.parser")

        table = soup.find("table", class_="table table-striped")
        for tr_tag in table.find_all("tr"):
            a_tag = tr_tag.find("a")
            if a_tag == None:
                continue
            url1 = "http://soeasycenter.com" + a_tag["href"]
            tds = tr_tag.find_all("td")
            date = tds[3].text
            se=self.url_increment.is_increment(url1,date)
            print(se)
            if se:
                urls.append(url1)
        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
        urls = []
        for i in range(1000):
            urls.append(str(url)+"_"+str(i))
        return urls


class thrid(ss.ThreadingSpider):
    def get(self,url):
        print("222222")
        html = get_html(url)

        soup = BeautifulSoup(html, "html.parser")

        div_tag = soup.find("div", class_="maincontent")
        fdiv = div_tag.find("div", class_="mytop")
        title = fdiv.find("h4").get_text().strip()
        date = fdiv.find("p").get_text().strip()
        b_num = re.search("发布时间：", date).span()
        e_num = re.search("来源：", date).span()
        date = date[b_num[1]:e_num[0]].strip()
        text = div_tag.find("div", class_="mymain").get_text().strip()
        text = "".join(text.split())

        line = url + "##" + date + "##" + title + "##" + text+"\n"
        return line





if __name__ == '__main__':

    j = job.Job("test0103")
    j.set_speed()
    j.submit("first","thrid",pyname="test")

