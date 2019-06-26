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