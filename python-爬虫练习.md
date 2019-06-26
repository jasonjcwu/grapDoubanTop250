---
title: python 爬虫练习
categories: python
tags: [爬虫, 练习]
---

# python 爬虫练习五个小练习

### 值得注意的点

* 使用xpath爬取的是一个list要取list[0]得到字符串

* 一些格式，生数据处理，

    使用```strip(),lstrip(),rstrip()```

    * Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。  

        **注意：** 该方法只能删除开头或是结尾的字符，不能删除中间部分的字符

    * 使用正则删除多余字符

        ```b = re.compile()``````b.findall()```

        python暂时只会这个正则方法，reg匹配所有编程语言都是通用的

* xpath(....../text())获取文本

* 有些地方爬取的内容为空，运行就会报错，用if 判断xpath内容是否为空，else写入空内容的通用值

### 整体思路

从控制台找到要爬取的信息，无非就是html内容，json内容，ajax请求内容,获取到节点，写入字典，导出json

跟老师不同的是，删除了一些函数，写在一个里，因为python本身就是脚本编程语言，一行语句写一个函数无疑加大了代码阅读难度。精简代码行，可读性提高，小demo没有维护的实施性。

### 内容





### 爬取内容

**1.豆瓣音乐top250**  
url：https://music.douban.com/top250  
爬取歌名，作者，评分

* 跟豆瓣电影类似

```python
import requests, json, xlwt, re, time
from lxml import html


class TopMusicSpider:

    def __init__(self):
        self.url_temp = " https://music.douban.com/top250?start={}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}

    # 爬取数据返回json
    def run(self):
        etree = html.etree  # 引入lxml
        url_list = []
        content_list = []
        b = re.compile('^(.*?)/')
        for i in range(10):
            url_list.append(self.url_temp.format(i*25))
            #  lxml解析文章（http请求，把user-Agent浏览器代理写入http头,模拟用户操作防止被检测，
            # decode（）将内容解码)
            response = etree.HTML(requests.get(url_list[i], headers=self.headers).content.decode())
            div_list = response.xpath('//div[@class="pl2"]')  # 获取当前页节点列表
            for div in div_list:  # 循环节点，分别在每个节点里面取内容
                item = dict()
                item['title'] = div.xpath('./a[1]/text()')[0].strip() # 提取题目
                item['author']= b.findall(div.xpath('./p/text()')[0])[0]
                item['start'] = div.xpath('./div/span[@class="rating_nums"]/text()')[0]
                content_list.append(item)
            print("已爬取{}页".format(i+1))
            #time.sleep(1)
        print(content_list)
        return content_list
    # 写入文件夹，缩进2空格
    def jsonToTxt(self):
        jsonmusic = self.run()
        with open("topmusic.json", 'a', encoding='utf-8') as f:  # 也可以改成.txt文件
            f.write(json.dumps(jsonmusic, ensure_ascii=False, indent=2))


TopMusicSpider().jsonToTxt()

```



**2.理论文选**  
url：http://www.qstheory.cn/qszq/llwx/index.htm  
爬取标题，作者，来源，日期

```python
import requests, json, xlwt, re, time
from lxml import html


class truethSpider:

    def __init__(self):
        self.url = "http://www.qstheory.cn/qszq/llwx/index.htm"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}

    # 爬取数据返回json
    def run(self):
        etree = html.etree  # 引入lxml
        content_list = []
            #  lxml解析文章（http请求，把user-Agent浏览器代理写入http头,模拟用户操作防止被检测，
            # decode（）将内容解码)
        response = etree.HTML(requests.get(self.url, headers=self.headers).content.decode())
        div_list = response.xpath('//div[@class="list-style1 row"]/ul/li')  # 获取当前页节点列表
        for div in div_list:  # 循环节点，分别在每个节点里面取内容
            item = dict()
            item['title'] = div.xpath('./a/text()')[0]  # 提取题目
            if div.xpath('./div/span[1]/text()') :
                item['author'] = div.xpath('./div/span[1]/text()')[0]  # 作者
            else :
                item['author']='匿名'
            item['from'] = div.xpath('./div/span[2]/text()')[0].lstrip('来源-')  # 来源
            item['date'] = div.xpath('./div/span[3]/text()')[0]  # 日期
            content_list.append(item)
        print(content_list)
        return content_list
    # 写入文件夹，缩进2空格
    def jsonToTxt(self):
        jsonNet = self.run()
        with open("truethNet.json", 'a', encoding='utf-8') as f:  # 也可以改成.txt文件
            f.write(json.dumps(jsonNet, ensure_ascii=False, indent=2))


truethSpider().jsonToTxt()
```



**3.金程考研**  
url：http://www.51dx.org/review/index.shtml  
爬取标题，文本

```python
import requests, json, xlwt, re, time
from lxml import html


class kaoyanSpider:

    def __init__(self):
        self.url_temp = "http://www.51dx.org/review/index{}{}.shtml"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}

    # 爬取数据返回json
    def run(self):
        etree = html.etree  # 引入lxml
        url_list = []
        content_list = []
        for i in range(199):
            if i < 1:
                url_list.append(self.url_temp.format('', ''))
            else :
                url_list.append(self.url_temp.format('_', i+1))
             #  lxml解析文章（http请求，把user-Agent浏览器代理写入http头,模拟用户操作防止被检测，
            # decode（）将内容解码)
            response = etree.HTML(requests.get(url_list[i], headers=self.headers).content.decode())
            div_list = response.xpath('//div[@class="listSingle"]/div[@class="text"]')  # 获取当前页节点列表
            for div in div_list:  # 循环节点，分别在每个节点里面取内容
                item = dict()
                item['title'] = div.xpath('./div/a/@title')[0] # 提取题目
                if div.xpath('./h3/text()'):
                    item['intro'] = div.xpath('./h3/text()')[0]
                else:
                    item['intro'] = ' '
                content_list.append(item)
            print("已爬取{}页".format(i+1))
            #time.sleep(1)
        #print(content_list)
        return content_list
    # 写入文件夹，缩进2空格
    def jsonToTxt(self):
        jsonNet = self.run()
        with open("kaoyan.json", 'a', encoding='utf-8') as f:  # 也可以改成.txt文件
            f.write(json.dumps(jsonNet, ensure_ascii=False, indent=2))


kaoyanSpider().jsonToTxt()
#kaoyanSpider().run()
```



**4.携程酒店**  
url：https://hotels.ctrip.com/hotel/changde201#ctm_ref=hod_hp_sb_lst  
爬取常德酒店名，地址，评分

* 携程最开始用**Selenium**库但是爬到第二页，内容获取报错，很奇怪。有时候下一页按钮也获取不到，这个库没学什么，试了多次所以放弃了，用回了requests

```python
from lxml import html
import time, re,requests
import json

temp_url=('https://hotels.ctrip.com/hotel/changde201/p{}')
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}
stripD = re.compile('[^\d*]')
etree = html.etree  # 引入lxml


def run():
    for i in range(15):
        response = etree.HTML(requests.get(temp_url.format(i+1), headers=headers).content.decode())
        li_list = response.xpath('//ul[@class="hotel_item"]')
        content_list = []
        for li in li_list:
            item = dict()
            # 使用正则把左边数字去掉，然后join合并成string
            item['hotel_name'] = "".join(stripD.findall(li.xpath('./li/h2/a/text()')[0]))
            # 把左右的垃圾信息去掉
            item['hotel_address'] = "".join(li.xpath('./li/p[@class="hotel_item_htladdress"]/text()')).lstrip("【 】").rstrip("。 ")
            # 判断有无评分
            if li.xpath('./li/div[@class="hotelitem_judge_box"]/a/span[@class="hotel_value"]/text()'):
                item['start'] = li.xpath('./li/div[@class="hotelitem_judge_box"]/a/span[@class="hotel_value"]/text()')[0]
            else:
                item['start']="暂无评分"
            print(item)
            content_list.append(item)

        with open('cstrip.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(content_list, ensure_ascii=False, indent=2))
        print("爬了{}页".format(i+1))
run()
```



**5.斗鱼直播**  
爬取房间信息

* 直接找到开发者工具Network里的json文件

```python
import requests
import json

# 请求json数据的url
url_temp = "https://www.douyu.com/gapi/rkc/directory/0_0/{}"
header = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
#发送请求获取响应

def run():
    for i in range(10):
        url=url_temp.format(i)
    #2.遍历，发送请求获取响应
        response = requests.get(url, headers=header).content.decode()
        #3.提取数据
        dict = json.loads(response)
        # 取到data的值
        data = dict['data']
        # 取到rl的值(注意，rl的值是一个列表，里面有120个字典元素，每个字典表示一个房间信息)
        rl = data['rl']
        content_list = []
        for li in rl:
            item = {}
            # 房间
            item['room_name'] = li['rn']
            item['author_name'] = li['nn']
            item['room_cate'] = li['c2name']
            print(item)
            content_list.append(item)
        #4.保存
        with open('douyu.txt', 'a', encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=2))
run()

```

