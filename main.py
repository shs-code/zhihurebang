# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',   
    'cookie':''}  #用cookie信息，自行添加

text = requests.get("https://www.zhihu.com/hot",headers=headers).text
main_page = BeautifulSoup(text,"html.parser")
table = main_page.find("div",{"class":"HotList-list"})  #把想要的找到

title = table.find("h2",{"class":"HotItem-title"}).text #标题
print(title)
excerpt = table.find('p', class_='HotItem-excerpt').text #题目内容
print(excerpt)
website = table.find('a').get('href')             #网址
print(website)
hot = table.find('div',class_="HotItem-metrics HotItem-metrics--bottom").text.replace('\u200b分享','') #热度，去掉'分享'
print(hot)

#没问题就写个批量
datai = []
n=0
for i in table:
    n+=1
    #print(i.text)
    dic = {}
    dic['Title'] = i.find('h2',class_='HotItem-title').text
    try:
        dic['Excerpt'] = i.find('p', class_='HotItem-excerpt').text
    except AttributeError:
        pass
    dic['Website'] = i.find('a').get('href')       
    try:
        dic['Hot'] = i.find('div',class_="HotItem-metrics HotItem-metrics--bottom").text.replace('\u200b分享','')
    except AttributeError:
        pass
    datai.append(dic)
        # 分别获取字段内容
    # print('成功采集%i条数据' % n)  在for循环内可以检查哪一条爬取失败  
print('成功采集共%i条数据' % n)    
datai[:2]

df = pd.DataFrame(datai)
ndf= df.fillna('如题') #有些题目内容是空白，即是题目标题
