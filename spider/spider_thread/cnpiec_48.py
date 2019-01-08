
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
        for i in range(500):
            urls.append("http://www.bidchance.com/search.do?currentpage="+str(i+1)+"&province=&channel=gonggao&queryword=&searchtype=sj&bidfile=&recommend=&leftday=&searchyear=&field=all&displayStyle=title&attachment=&starttime=&endtime=&pstate=")
        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
        urls = []
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                " Chrome/70.0.3538.102 Safari/537.36",
                  "Cookie": '__jsluid=fda97a093bd3c210c560f9ab4ecb80dd;'
                            ' reg_referer="aHR0cDovL3d3dy5iaWRjaGFuY2UuY29tLw=="; '
                            'Hm_lvt_2751005a6080efb2d39109edfa376c63=1546582829; bdshare_firstime=1546582832885;'
                            'Cookies_Userid=42k6u0p1egikh7r0p2b32ujavq0nu79; JSESSIONID=8A98DB3AA737DD13D1FB1F13FA992827;'
                            ' Hm_lpvt_2751005a6080efb2d39109edfa376c63=1546587128;'
                            ' Cookies_Key=-3k1utnkf0g7gt5lte5pf4tu1um04u2el57nojam94jqirif80mre9ccdmgj8b6ci;'
                            'Cookies_token=208e686e-c944-49b9-8e8c-f24e25baecac'}
        time.sleep(5)
        data = requests.get(url, headers=header)
        data.encoding = "GBK"
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        div_tag = soup.find("div", class_="searchaltab")
        for tr in div_tag.find_all("tr", class_="datatr"):
            a = tr.find("a")
            url_n = a["href"]
            td = tr.find_all("td")
            date = td[td.__len__() - 1].text
            result=self.url_increment.is_increment(url_n,date)
            if result:
                urls.append(url_n)
        return urls


class thrid(ss.ThreadingSpider):
    def get(self,url):
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                " Chrome/70.0.3538.102 Safari/537.36",
                  "Connection": "keep - alive",
                  "Cookie": '__jsluid=fda97a093bd3c210c560f9ab4ecb80dd; reg_referer="aHR0cDovL3d3dy5iaWRjaGFuY2UuY29tLw=="; Hm_lvt_2751005a6080efb2d39109edfa376c63=1546582829; bdshare_firstime=1546582832885; Cookies_Userid=42k6u0p1egikh7r0p2b32ujavq0nu79; JSESSIONID=B6FEB4E331F0946C6D62E44BE4855196; Cookies_Key=-3k1utnkf0g7gt5lte5pf4tu1um04u2el56kbnh90lmlnl35fd4ti94uqg7bcbrci; Cookies_token=0dd33210-eaf5-4e53-bcd5-c0a4c5a80b5b; Hm_lpvt_2751005a6080efb2d39109edfa376c63=1546590789'}
        time.sleep(5)
        resq = requests.get(url, headers=header)
        soup = BeautifulSoup(resq.text, "html.parser")

        title = soup.find("div", class_="xlh").text.strip()
        div_tag = soup.find("div", class_="xllabel-l")
        date = div_tag.find("span", id="infopubdate").text.strip()
        text = soup.find("div", class_="xlbodybox").text
        text = "".join(text.split())
        line = url + "##" + date + "##" + title + "##" + text+"\n"
        return line

def test():
    urls = []
    url="http://www.bidchance.com/search.do?currentpage=2&province=&channel=gonggao&queryword=&searchtype=sj&bidfile=&recommend=&leftday=&searchyear=&field=all&displayStyle=title&attachment=&starttime=&endtime=&pstate="
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                            " Chrome/70.0.3538.102 Safari/537.36",
              "Cookie":'__jsluid=fda97a093bd3c210c560f9ab4ecb80dd;'
                       ' reg_referer="aHR0cDovL3d3dy5iaWRjaGFuY2UuY29tLw=="; '
                       'Hm_lvt_2751005a6080efb2d39109edfa376c63=1546582829; bdshare_firstime=1546582832885;'
                       'Cookies_Userid=42k6u0p1egikh7r0p2b32ujavq0nu79; JSESSIONID=8A98DB3AA737DD13D1FB1F13FA992827;'
                       ' Hm_lpvt_2751005a6080efb2d39109edfa376c63=1546587128;'
                       ' Cookies_Key=-3k1utnkf0g7gt5lte5pf4tu1um04u2el57nojam94jqirif80mre9ccdmgj8b6ci;'
                       'Cookies_token=208e686e-c944-49b9-8e8c-f24e25baecac'}

    data = requests.get(url,headers=header)
    data.encoding = "GBK"
    data = data.text
    soup = BeautifulSoup(data, "html.parser")
    div_tag=soup.find("div",class_="searchaltab")
    for tr in div_tag.find_all("tr",class_="datatr"):
        # print(tr)
        a=tr.find("a")
        url_n=a["href"]
        td =tr.find_all("td")
        date=td[td.__len__()-1].text
        print(url_n,date)
    return urls


def test2():
    url="http://www.bidchance.com/info-gonggao-35504293.html"
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                            " Chrome/70.0.3538.102 Safari/537.36",
              "Connection": "keep - alive",
              "Cookie": '__jsluid=fda97a093bd3c210c560f9ab4ecb80dd; reg_referer="aHR0cDovL3d3dy5iaWRjaGFuY2UuY29tLw=="; Hm_lvt_2751005a6080efb2d39109edfa376c63=1546582829; bdshare_firstime=1546582832885; Cookies_Userid=42k6u0p1egikh7r0p2b32ujavq0nu79; JSESSIONID=B6FEB4E331F0946C6D62E44BE4855196; Cookies_Key=-3k1utnkf0g7gt5lte5pf4tu1um04u2el56kbnh90lmlnl35fd4ti94uqg7bcbrci; Cookies_token=0dd33210-eaf5-4e53-bcd5-c0a4c5a80b5b; Hm_lpvt_2751005a6080efb2d39109edfa376c63=1546590789'}
    resq=requests.get(url,headers=header)
    soup = BeautifulSoup(resq.text, "html.parser")


    title = soup.find("div", class_="xlh").text.strip()
    print(title)

    div_tag = soup.find("div", class_="xllabel-l")
    date = div_tag.find("span", id="infopubdate").text.strip()
    print(date)
    text = soup.find("div", class_="xlbodybox").text
    text = "".join(text.split())
    print(text)


def login():
    session=requests.session()
    login_url="http://www.bidchance.com/ssologin.do?method=bidchanceLoginPost"
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
    user_info={"userid":"cnpiec","pwd":"cnpiec","submit":"登录"}

    resq=session.post(login_url,data=user_info,headers=header)
    print(resq.text)
    url = "http://www.bidchance.com/info.do?channel=gonggao&id=35473267&q="
    result=session.get(url,headers=header)
    soup = BeautifulSoup(result.text, "html.parser")




if __name__ == '__main__':
    # test()
    j = job.Job("cnpiec_48")
    j.set_speed()
    j.submit("first","second","thrid",pyname="cnpiec_48")

