# -*- coding: utf-8 -*-
import traceback
import re
import requests
from bs4 import BeautifulSoup
import time
def getTVHtml(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("html wrong")
        return ''

def getSeasonHtml(name, season, html): #返回如纸牌屋第一季页面的链接

    soup = BeautifulSoup(html, "html.parser")
    href = ''
    try:
        mainTag = soup.find_all('div', attrs = 'archive_box')
        for i in mainTag:
            """
            seasonTag1用来匹配标题（有可能会出现标题对不上如老友记第六至九季）
            这时候就需要seasonTag2了即匹配该美剧的简介，仔细观察简介会发现可能出现
            美剧名+季数如老友记第二、三、四季
            """
            seasonTag1 = re.findall(name + r'第.{0,10}' + season[1 : -1] + '.{0,10}季', i.h2.a.string)
            seasonTag2 = re.findall(name + r'第.{0,10}' + season[1 : -1] + '.{0,10}季', str(i.find_all('div', attrs = 'archive')[0]).replace(' ', ''))
            if seasonTag1 or seasonTag2:
                #print(i.find_all('span', attrs = 'archive_more'))
                href = re.findall('href=\".*?\"', str(i.h2))[0][6 : -1]
                return href
        return href          
                    
    except:
        print("season html wrong")
        pass 
       
def getDramaUrl(href):
    if href == '':
        print("没有该剧")
        return
    html = getTVHtml(href)
    #直接匹配要吗是e开头的下载链接，要吗是m开头的下载链接，也有可能是t开头的
    urllist = re.findall(r'href=\"[emt].*?\"', html)
    return urllist
def outputUrl(name, season, urllist):
    #结果输出到.txt文件
    try:
        if urllist == []:
            print('没有资源')
            return
        
        with open(name + season + 'urllist.txt', 'w', encoding = 'utf-8') as f:
            for i in range(len(urllist)):
                f.write(urllist[i][6 : -1] + '\n')
            f.close()
    except:
        print("outputurl wrong")
        pass

#process——Info为封装函数被getDramaGUI.py所调用``
def process_Info(name, season):
    
    url = 'http://cn163.net/?s=' + name
    
    html = getTVHtml(url)
    
    href = getSeasonHtml(name, season, html)
    urllist = getDramaUrl(href)

    outputUrl(name, season, urllist)
    

    
    
