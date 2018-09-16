#!/usr/bin/env python
# coding=utf-8
from urllib import request
import re
import requests
import json
import os
from faker import Factory
from bs4 import BeautifulSoup


def get_html(url):
    f=Factory.create()
    ua=f.user_agent()
    print(ua)
    data = requests.get( url ,headers={"Uesr-Agent":ua})
    data.encoding = 'gbk'
    data = data.text
    return data

url = "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/t20180911_1025538.html"

print(get_html(url))


