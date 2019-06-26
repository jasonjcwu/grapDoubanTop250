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