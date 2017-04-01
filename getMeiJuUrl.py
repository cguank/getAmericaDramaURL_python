# -*- coding: utf-8 -*-
import traceback
import re
import requests
from bs4 import BeautifulSoup
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
        #季数的链接都保存到了div大标签下，不同的div有不同的季数
        mainTag = soup.find_all('div', attrs = 'archive_title')
        for tagDiv in mainTag:
            #div下的a标签保存了季数的http链接
            seasonUrlTag = tagDiv.find_all('a')[0]
            #美剧名+季数用来匹配符合条件的季数链接
            if re.findall(name + season, str(seasonUrlTag)):
                href = re.findall(r'\"http.*?\"', str(seasonUrlTag))[0][1 : -1]
                return href
            #可能美剧名在a标签下是英文名这时候中文美剧名就匹配不到了 
            #因此我想直接匹配季数 再确定这个页面是符合条件的美剧 即直接在该页面搜索该美剧名
            #注意and后面的匹配是匹配整个页面而不是匹配a标签下、
            #建议可以直接取天天美剧网查找权利的游戏，其结果是英文名Games of Thrones
            elif re.findall(season, str(seasonUrlTag)) and re.findall(name, str(soup)):
                href = re.findall(r'\"http.*?\"', str(seasonUrlTag))[0][1 : -1]
                return href
        
    except:
        print("season html wrong")
        pass
       
def getDramaUrl(href):
    if href == '':
        print("没有该剧")
        return
    html = getTVHtml(href)
    #直接匹配要吗是e开头的下载链接，要吗是m开头的下载链接
    urllist = re.findall(r'href=\"[em].*?\"', html)
    return urllist
def outputUrl(name, season, urllist):
    #结果输出到.txt文件
    try:
        if urllist == []:
            print('没有资源')
            return
        with open('urllist_README.txt', 'w') as f:
            f.write(name + season + '\n' + '说明：链接中有的是重复链接或者清晰度不同的链接，或者是该季的集合\n可用迅雷下载链接并可在迅雷中查看集数，\n可能会找不到资源\n在迅雷新建任务中可一次性复制多个链接\n')
            f.close()
        with open('urllist.txt', 'w') as f:
            for i in range(len(urllist)):
                f.write(urllist[i][6 : -1] + '\n')
            f.close()
    except:
        traceback.print_exc()
        print("outputurl wrong")
        pass

#process——Info为封装函数被getDramaGUI.py所调用``
def process_Info(name, season, path = 'urllist.txt'):
    
    url = 'http://cn163.net/?s=' + name
    
    html = getTVHtml(url)
    
    href = getSeasonHtml(name, season, html)
    
    urllist = getDramaUrl(href)
    
    outputUrl(name, season, urllist)

