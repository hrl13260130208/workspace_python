from bs4 import BeautifulSoup
import requests
from configparser import ConfigParser
import PyPDF2
from collector.name_manager import json_conf_bean,template_manager
import os
import logging
from collector.errors import NoConfError
import time
import copy



logger = logging.getLogger("logger")

class config_parser():
    def __init__(self,*file_name):
        self.conf = ConfigParser()
        self.tm = template_manager()
        self.backup_file="C:/pdfs/backup"
        if file_name:
            self.file_name=file_name
        else:
            self.file_name = "conf.cfg"

    def test(self,section,url,*config):
        if config:
            self.conf.read(config)
        else:
            self.conf.read(self.file_name)
        conf_test=self.conf.items(section)
        return  HTML(None,None,None).test(conf_test,url)

    def get_section(self,section):
        self.conf.read(self.file_name)
        return self.conf.items(section)

    def paser(self):
        self.conf.read(self.file_name)
        sections=self.conf.sections()
        for section in sections:
            rne=section.split("_")
            jcb=json_conf_bean(rne[0],rne[1])
            jcb.set_conf(self.conf.items(section))
            self.tm.save(jcb)
    def backup(self):
        file=open(self.backup_file,"w")
        for sourcename in self.tm.get_conf_name():
            for conf in self.tm.get_eissns(sourcename):
                if not self.tm.is_default_key(conf):
                    file.write(sourcename+"#"+conf+"#"+self.tm.get_conf_string(conf)+"\n")

    def read_backup(self):
        file=open(self.backup_file)
        for line in file.readlines():
            args=line.split("#")
            jcb=json_conf_bean(args[0],args[1])
            jcb.paser(args[2])
            self.tm.save(jcb)






class HTML():
    def __init__(self,eb,jcb,tm):
        self.eb=eb
        self.jcb=jcb
        self.tm=tm

    def run(self,url):
        if self.load(self.jcb):
            logger.info("load secuess")
            return self.do_run(self.jcb.conf,url)
        else:
            logger.info("load faild, start find a conf from default.")
            confs=self.tm.get_default(self.jcb)

            logger.debug(self.jcb.get_sourcename()+" default: "+str(confs))

            for conf in confs:
                new_jcb=json_conf_bean(self.jcb.get_sourcename(),self.eb.eissn)
                new_jcb.paser(conf)
                if self.test(new_jcb.conf,url):
                    logger.info("find a conf form default!")

                    self.tm.save(new_jcb)
                    return self.do_run(new_jcb.conf,url)
            logger.error("There is no conf available!")
            raise NoConfError("no conf")

    def load(self,jcb):
        string= self.tm.get(jcb)
        if string :
            jcb.paser(string)
            return True
        else:
            return False

    def test(self,conf,url):
        copy_conf=copy.deepcopy(conf)
        result=None
        try:
            result=self.do_run(copy_conf,url)
        except:
            result=None
        return result !=None


    def do_run(self,conf,url):
        url_s=""
        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        conf.sort()
        last = conf[conf.__len__() - 1]
        if last[0] == "url":
            url_s = last[1]
            conf.remove(last)
        return  self.run_url(url_s,conf,soup)

    def run_url(self,url_s,conf,soup):

        first =conf[0]
        url = self.get_url(first[1],soup)
        conf.remove(first)
        logger.debug("url : "+url)
        if conf.__len__() == 0:
            return url_s+url
        else:
            html = get_html(url)
            new_soup = BeautifulSoup(html, "html.parser")
            return  self.run_url(url_s,conf,new_soup)

    def get_url(self,string,soup):
        strs=string.split(";")
        logger.debug("Strings split by ; is : "+str(strs))
        tag=self.find(strs,soup)
        return tag.find("a")["href"]

    def find(self,strs,soup):
        first_args=strs[0]
        args=first_args.split(",")
        logger.debug("Strings split by , is : "+ str(args))
        tag=soup.find(args[0],attrs={args[1]:args[2]})
        strs.remove(first_args)

        if strs.__len__() == 0:
            return tag
        else:
            return  self.find(strs,tag)



header={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}

def get_html(url):
    time.sleep(2)
    data = requests.get(url,headers=header,verify=False,timeout=20)
    data.encoding = 'utf-8'
    datatext = data.text
    data.close()
    return datatext

def download(url, file):
    time.sleep(2)
    data = requests.get(url, headers=header,timeout=30)
    data.encoding = 'utf-8'
    file = open(file, "wb")
    file.write(data.content)

def checkpdf(file):
    pdf = PyPDF2.PdfFileReader(file)
    return pdf.getNumPages()





if __name__ == '__main__':
    cp = config_parser()
    cp.read_backup()



    # url="http://dx.doi.org/10.2478/ttj-2018-0031"
    # cp=config_parser()
    # res=cp.get_section("Gruyter_2255-8683-2255-8691")
    # print(cp.test("Wiley_2150-8925-2150-8925",url))


