# 爬取豆瓣Top250
> 语言：python  
使用库：requests(http请求数据), json(字典与json转换), xlwt(json与excel),lxml(解析xml，xpath)  
爬取内容：豆瓣电影，图书，音乐Top250
---
### 主要方法步骤
* 使用requests请求网页url，然后使用lxml把网页html解析解析下来
* 获取信息区块列表
* 分别爬取区块想要的信息存入字典
* 写入文件保存

### 值得注意点
* 在使用pip安装的时候,由于是国外资源,下载速度很慢,可以使用国内镜像, 在cdm中输入   
```pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests(填库名) ```
* 获取节点方法  
1.使用XPath获取节点[XPath语法](http://www.w3school.com.cn/xpath/xpath_syntax.asp)  
去chrome插件市场下载 XPath Helper(方便检查)  
[CssSelector组件将CSS选择器转换为XPath表达式](https://symfony.com/css-selector)  
> **为什么要使用CSS选择器？**  
当您解析HTML或XML文档时，到目前为止最强大的方法是XPath。  
XPath表达式非常灵活，因此几乎总有一个XPath表达式可以找到您需要的元素。不幸的是，它们也变得非常复杂，学习曲线也很陡峭。即使是常见的操作（例如查找具有特定类的元素）也可能需要冗长且难以处理的表达式。  
许多开发人员 - 尤其是Web开发人员 - 更习惯使用CSS选择器来查找元素。除了在样式表中工作之外，CSS选择器还在JavaScript中使用，querySelectorAll()并且在jQuery，Prototype和MooTools等流行的JavaScript库中使用。  
CSS选择器的功能不如XPath，但更容易编写，阅读和理解。由于它们功能较弱，几乎所有的CSS选择器都可以转换为XPath等价物。然后，此XPath表达式可以与使用XPath查找文档中的元素的其他函数和类一起使用。

2.学前端的我觉得beautifulsoup很好用，因为直接css选择器获取节点，十分方便  
安装```$ pip install beautifulsoup4```  
[beautifulsoup4中文文档](https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/)

### 主要代码

```python
import requests, json, xlwt
from lxml import html


class TopMoviesSpider:

    def __init__(self):
        self.url_temp = "https://movie.douban.com/top250?start={}&filter="
        # https://book.douban.com/top250?start={} 爬取豆瓣图书Top250
        # https://music.douban.com/top250?start=25 豆瓣音乐Top250 节点可能有些不同写不同的xpath
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}

    # 爬取数据返回json
    def run(self):
        etree = html.etree  # 引入lxml
        url_list = []
        content_list = []
        for i in range(10):
            url_list.append(self.url_temp.format(i*25))
            #  lxml解析文章（http请求，把user-Agent浏览器代理写入http头,模拟用户操作防止被检测，
            # decode（）将内容解码)
            response = etree.HTML(requests.get(url_list[i], headers=self.headers).content.decode())
            div_list = response.xpath('//div[@class="info"]')  # 获取当前页节点列表
            for div in div_list:  # 循环节点，分别在每个节点里面取内容
                item = dict()
                item['author'] = div.xpath('.//div[@class="hd"]/a/span[1]/text()')[0]  # 提取题目
                item['start'] = div.xpath('.//div[@class="bd"]/div/span[@class="rating_num"]/text()')[0]  # 评分
                item['text'] = div.xpath('.//div[@class="bd"]/p[@class="quote"]/span/text()')[0]  # 简介
                item['url'] = div.xpath('.//div[@class="hd"]/a/@href')[0]  # 获取URL
                content_list.append(item)  # 添加到json列表末尾
        return content_list

    # 写入文件夹，缩进2空格
    def jsonToTxt(self):
         jsonMovie = self.run()
         with open("topmovies.json", 'a', encoding='utf-8') as f:  # 也可以改成.txt文件
            f.write(json.dumps(jsonMovie, ensure_ascii=False, indent=2))

    # 写入excel
    def jsonToexcel(self):
        jsonMovie = self.run()
        workbook = xlwt.Workbook()  # 引入wlwt,workbook模块
        sheet1 = workbook.add_sheet('TopMovie')
        execelhead = list(jsonMovie[0].keys())  # 获取键名写入标题
        for i in range(len(execelhead)):  # 标题写入头
            sheet1.write(0, i, execelhead[i])
        for j in range(0, len(jsonMovie)):  # 循环写入
            m = 0
            ls = list(jsonMovie[j].values())
            for k in ls:
                sheet1.write(j + 1, m, k)
                m += 1
        workbook.save('topmovies.xls')  #保存

TopMoviesSpider().jsonToTxt()
#TopMoviesSpider().jsonToexcel()
```

### 截图
![excel图](https://github.com/2249038142/grapDoubanTop250/blob/master/image/excel.png)
![json图](https://github.com/2249038142/grapDoubanTop250/blob/master/image/json.png)
