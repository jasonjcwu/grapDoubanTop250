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