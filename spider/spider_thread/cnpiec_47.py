
import requests
from bs4 import  BeautifulSoup
import spider.spider_modules.standard_spider as ss
import spider.spider_modules.job as job
import time



def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.ThreadingSpider):

    def get(self,url):
        urls = []
        urls.append("http://ecp.cnnc.com.cn/xzbgg/index.jhtml")
        for i in range(349):
            urls.append("http://ecp.cnnc.com.cn/xzbgg/index_"+str(i+2)+".jhtml")
        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
        urls=[]
        data = requests.get(url)
        data.encoding = "UTF-8"
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        div_tag = soup.find("div", class_="List1")
        for li in div_tag.find_all("ul"):
            a = li.find("a")["href"]
            url_n= "http://ecp.cnnc.com.cn" + a
            date = li.find("span", class_="Right Gray").text
            result=self.url_increment.is_increment(url_n,date)
            if result:
                urls.append(url_n)
        return urls


class thrid(ss.ThreadingSpider):
    def get(self,url):
        pass

        # line = url + "##" + date + "##" + title + "##" + text+"\n"
        # return line

def test():
    urls = []
    url="http://ecp.cnnc.com.cn/xzbgg/index.jhtml"

    data = requests.get(url)
    data.encoding = "UTF-8"
    data = data.text
    soup = BeautifulSoup(data, "html.parser")
    div_tag=soup.find("div",class_="List1")
    for li in div_tag.find_all("ul"):
        a=li.find("a")["href"]
        url="http://ecp.cnnc.com.cn"+a
        date=li.find("span",class_="Right Gray").text
        print(url ,date)

    return urls


def test2():
    url="http://ecp.cnnc.com.cn/xzbgg/64260.jhtml"
    resq=requests.get(url)
    resq.encoding = "UTF-8"
    data=resq.text
    soup=BeautifulSoup(data,"html.parser")
    div_tag=soup.find("div",class_="W980 Center PaddingTop10")
    title=div_tag.find("h1").text.strip()
    print(title)
    div_tag2=div_tag.find("div",class_="Padding10 TxtCenter Gray").text.strip()
    print(div_tag2)
    with open('111.txt','w',encoding='utf-8') as f:
        f.write(data)




    # title = soup.find("div", class_="xlh").text.strip()
    # print(title)
    #
    # div_tag = soup.find("div", class_="xllabel-l")
    # date = div_tag.find("span", id="infopubdate").text.strip()
    # print(date)
    # text = soup.find("div", class_="xlbodybox").text
    # text = "".join(text.split())
    # print(text)







if __name__ == '__main__':

    test2()
    # j = job.Job("cnpiec_47")
    # j.set_speed()
    # j.submit("first","second","thrid",pyname="cnpiec_47")

