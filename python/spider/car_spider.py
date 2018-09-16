#!/usr/bin/env python
# coding=utf-8
from urllib import request
import re
import requests
import json
import os
import sys


def img_spider(name_file):
    # 读取名单txt，生成包括所有物品的名单列表
    with open( name_file ) as f:
        name_list = [name.rstrip() for name in f.readlines()]
        print(name_list)
        f.close()
        # 遍历每一个物品，保存在以该物品名字命名的文件夹中
        fail_list=[]
    for name in name_list:
        # 生成文件夹（如果不存在的话）
        if not os.path.exists( '/data/tensorflow/dataset/car/' + name ):
            os.makedirs( '/data/tensorflow/dataset/car/' + name )
            # 修改range内数值n,可改变爬取数量为n*60
        print('start...')
        urls=[]
        try:
            urls=getManyPages(name,9)
        except:
            # 如果访问失败，就跳到下一个继续执行代码，而不终止程序
            print(name, "json have some errors！")
            fail_list.append(name)
        getImg(urls, '/data/tensorflow/dataset/car/' + name+'/')
    while(True):
        if fail_list.__len__()>0:
            for name in fail_list:
                # 生成文件夹（如果不存在的话）
                if not os.path.exists( '/data/tensorflow/dataset/car/' + name ):
                    os.makedirs( '/data/tensorflow/dataset/car/' + name )
                    # 修改range内数值n,可改变爬取数量为n*60
                print( 'failed start...' )
                urls = []
                try:
                    urls = getManyPages( name, 9 )
                    getImg( urls, '/data/tensorflow/dataset/car/' + name + '/' )
                    fail_list.remove( name )
                except:
                    # 如果访问失败，就跳到下一个继续执行代码，而不终止程序
                    print( name, "json have some errors！" )
                    fail_list.append( name )

            else:
                break


def getManyPages(keyword,pages):
    params=[]
    for i in range(30,30*pages+30,30):
        params.append({
                      'tn': 'resultjson_com',
                      'ipn': 'rj',
                      'ct': 201326592,
                      'is': '',
                      'fp': 'result',
                      'queryWord': keyword,
                      'cl': 2,
                      'lm': -1,
                      'ie': 'utf-8',
                      'oe': 'utf-8',
                      'adpicid': '',
                      'st': -1,
                      'z': '',
                      'ic': 0,
                      'word': keyword,
                      's': '',
                      'se': '',
                      'tab': '',
                      'width': '',
                      'height': '',
                      'face': 0,
                      'istype': 2,
                      'qc': '',
                      'nc': 1,
                      'fr': '',
                      'pn': i,
                      'rn': 30,
                      'gsm': '1e',
                      '1521206360261': ''
                  })
    url = 'https://image.baidu.com/search/acjson'
    urls = []
    for i in params:
        data = requests.get( url, params=i ).text
        data_json = json.loads( data )
        data_json = data_json.get( 'data' )
        for item in data_json:
            img_url= item.get( 'thumbURL' )
            urls.append(img_url)
    return urls

def getImg(dataList, localPath):

    if not os.path.exists(localPath):  # 新建文件夹
        os.mkdir(localPath)
    print(localPath)
    x = 0
    for i in dataList:
        if i != None:
            print('正在下载：%s' % i)
            ir = requests.get(i)
            open(localPath + '%d.jpg' % x, 'wb').write(ir.content)
            x += 1
        else:
            print('图片链接不存在')

if __name__ == '__main__':
    name_file = "/data/tensorflow/dataset/car/car_type_list.txt"
    img_spider( name_file )