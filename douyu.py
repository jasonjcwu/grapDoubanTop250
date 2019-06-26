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
