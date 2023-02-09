# -*- coding = utf-8 -*-
# @Time :2022/12/14 16:24
# @Author : 王俊庆
# @File : 单条爬取.py
# @Software : PyCharm


import requests
from my_fake_useragent import UserAgent
import os
import time
import tkinter as tk
import subprocess

def Url_analysis(url):
    url_temp = url.split('/')[-1]
    if '?' in url_temp:
        wb_id = url_temp.split('?')[0]
    else:
        wb_id = url_temp
    # print(wb_id)
    return wb_id


def mkdir(file_Folder_name):
    adress = os.getcwd()
    path = adress + '\\' + file_Folder_name
    print("图片保存路径为：" + path)
    isExists = os.path.exists(path)
    # print(isExists)
    if not isExists:
        # 如果不存在则创建目录,创建目录操作函数
        '''
        os.mkdir(path)与os.makedirs(path)的区别是,当父目录不存在的时候os.mkdir(path)不会创建，os.makedirs(path)则会创建父目录
        '''
        # 此处路径最好使用utf-8解码，否则在磁盘中可能会出现乱码的情况
        os.makedirs(path)
        print(path + ' 创建成功')
        return path
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return path


def current_date():
    temp = time.localtime(time.time())
    return temp


headers0 = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46',
    'Referer': 'https://www.weibo.com/',
    'Connection': 'keep-alive'
}
headers = {
    'cookie': 'SINAGLOBAL=6915506855981.115.1636270307855; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5CEbmxYRzHJuHImBHi4Xj85JpX5KMhUgL.FoqNehBceKzpe0n2dJLoIXeLxK-LB.eL1h5LxK-LB.eL1h5LxK-LB.qL1heLxK-LB.qL1heLxKqLB-qL12qLxKBLBonL1h5LxK-LBKBLBKLk--8x; ULV=1670815945351:62:11:2:3136894285858.7314.1670815945305:1670755852199; ALF=1673517061; SSOLoginState=1670925061; SCF=Ai7zbn4w0P3wWDaL2Y_X7c0PXxh3N77N0lRjQmdN9fYDwPsE91eprdqUJM_gKR7EfERkSx5w5qY6B4cj30LZmQQ.; SUB=_2A25OnDtVDeRhGeBJ61YX8SzNyDSIHXVt6CudrDV8PUNbmtANLXXRkW9NRnUWtZym8XdptZOZy2yNykCRRsAgl7tt; XSRF-TOKEN=rVRzkE-VQakbvD8XVYC9L-uC; WBPSESS=9w7uZ6TaXDDhKjNZA_cLcxTup9xu7m7MA7NDTZWF3d1RVOp49hEagkpgj8JcNMmVwSPG4UgKquA3dv9cK-4qhHGDREQiFeupYr9SK9fmB20-n2rambzRbyBJb0s9D1WW14stcyRmKmfCJHA0TbxvIA==; PC_TOKEN=10d7c567f7',
    'referer': 'https://weibo.com/5951386664/MjyuxvDx7?pagetype=homefeed',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46'
}

proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809'
}

if __name__ == '__main__':

    date = current_date()
    year, month, day, hour, minutes, sec = date[0], date[1], date[2], date[3], date[4], date[5]
    file_Folder_name = 'pic_' + str(year) + str(month) + str(day) + str(hour) + str(minutes) + str(sec)
    URL = input("请输入微博网址：")
    wb_id = Url_analysis(URL)

    url = f'https://weibo.com/ajax/statuses/show?id={wb_id}'
    resp = requests.get(url, headers=headers)
    # print(resp.text)

    json_data = resp.json()
    # print(json_data)

    num = 1

    root_path = mkdir(file_Folder_name)

    pic_ids = json_data["pic_ids"]
    pic_infos = json_data["pic_infos"]
    print("正在保存中……")
    for item in pic_ids:
        pic_url = pic_infos[f"{item}"]["largest"]["url"]
        # print(pic_url)

        img = requests.get(pic_url, headers=headers0).content
        save_path = root_path + '\\' + str(num) + ".jpg"
        # print(save_path)
        num += 1
        with open(save_path, "wb")as f:
            f.write(img)
    print("保存成功！！！")

'''
    if pic_ids:
        print("正在保存中，请稍等~")
        # 假设请求主页wx1.sinaimg.cn 和wx2.sina.img.cn无区别
        # url_host = 'https://wx1.sinaimg.cn/large/'
        url_host = 'https://wx2.sinaimg.cn/large/'
        # url_host = 'https://wx1.sinaimg.cn/mw2000/'
        # url_host = 'https://wx1.sinaimg.cn/mw2000/'
        # url_host = 'https://wx4.sinaimg.cn/large/'
        # url_host = 'https://wx1.sinaimg.cn/mw2000/'
        # url_host = 'https://zzx.sinaimg.cn/large/'
        for li in pic_ids:
            real_url = url_host + li + '.jpg'
            # print(real_url)
            img = requests.get(real_url, headers=headers0).content
            save_path = root_path + '\\' + str(num) + ".jpg"
            # print(save_path)
            num += 1
            with open(save_path, "wb")as f:
                f.write(img)
        print("保存成功！！！")
'''
