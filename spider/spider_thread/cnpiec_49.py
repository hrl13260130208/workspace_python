from concurrent.futures import  ThreadPoolExecutor,as_completed,Future
import requests
from bs4 import  BeautifulSoup
import spider.spider_modules.standard_spider as ss
import spider.spider_modules.name_manager as nm
import spider.spider_modules.job as job
import re
import datetime



def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.ThreadingSpider):

    def get(self,url):
        urls = []
        url = "http://htgs.ccgp.gov.cn/GS8/contractpublish/search"

        data = requests.get(url)
        data.encoding = "utf-8"
        data = data.text

        soup = BeautifulSoup(data, "html.parser")
        div_tag = soup.find("div", class_="pagigation")

        script_tags = div_tag.find_all("script")
        pages = script_tags[1].text
        start = pages.index("size:")
        print(type(start))
        end = pages.index(",", 7)
        num = int(pages[start + 5:end])
        urls.append("http://htgs.ccgp.gov.cn/GS8/contractpublish/index")
        for i in range(num - 1):
            urls.append("http://htgs.ccgp.gov.cn/GS8/contractpublish/index_" + str(i + 2))
        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
        urls = []

        data = requests.get(url)
        data.encoding = "utf-8"
        data = data.text

        soup = BeautifulSoup(data, "html.parser")
        ul_tag = soup.find("ul", class_="ulst")
        li_tags = ul_tag.find_all("li", style="height:60px")
        for li_tag in li_tags:
            a = li_tag.find("a")
            url_n = "http://htgs.ccgp.gov.cn/GS8/contractpublish" + a["href"][1:]
            string = li_tag.text
            start = string.index("发布时间：")
            end = string.index("采购人：")
            date=string[start + 5:end].strip()
            result=self.url_increment.is_increment(url_n,date)
            if result:
                urls.append(url_n)
        return urls


class thrid(ss.ThreadingSpider):
    def get(self,url):
        data = requests.get(url)
        data.encoding = "utf-8"
        data = data.text

        soup = BeautifulSoup(data, "html.parser")
        head = soup.find("div", class_="vT_detail_header")
        title = head.find("h2").text.strip()
        time = head.find("span", id="pubTime").text.strip()
        text = soup.find("div", class_="vT_detail_content w900c").text
        text = "".join(text.split())

        line =self.names.name +url + "##" + time + "##" + title + "##" + text+"\n"
        return line

def test():
    urls = []
    url="http://htgs.ccgp.gov.cn/GS8/contractpublish/index"
    data = requests.get(url)
    data.encoding = "utf-8"
    data = data.text

    soup = BeautifulSoup(data, "html.parser")
    ul_tag = soup.find("ul", class_="ulst")
    li_tags = ul_tag.find_all("li", style="height:60px")
    for li_tag in li_tags:
        a = li_tag.find("a")
        url_n = "http://htgs.ccgp.gov.cn/GS8/contractpublish" + a["href"][1:]
        string = li_tag.text
        start = string.index("发布时间：")
        end = string.index("采购人：")
        date = string[start + 5:end]
        print(url_n,date)
        date=date.strip()
        url_date = datetime.datetime.strptime(date,"%Y-%m-%d" )
        print(url_date)
        #result = url_increment.is_increment(url_n, date)
        # if result:
        #     urls.append(url_n)
    return urls


if __name__ == '__main__':
    j = job.Job("cnpiec_49")
    j.set_speed()
    j.submit("first","second","thrid",pyname="cnpiec_49")

