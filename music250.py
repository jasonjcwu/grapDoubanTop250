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
