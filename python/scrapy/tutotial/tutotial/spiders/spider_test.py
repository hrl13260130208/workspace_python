

import scrapy

class Spider_Test(scrapy.Spider):
    name="test"
    start_urls=["http://cz.fjzfcg.gov.cn/3500/openbidlist/f9ebc6637c3641ee9017db2a94bfe5f0/"]


    def parse(self, response):
        filename = response.text
        print("dsd:",filename)

