from selenium import webdriver
import time
import json

def run():
    driver = webdriver.Chrome()
    driver.get('https://www.huya.com/l')
    content_list=[]
    li_list = driver.find_elements_by_xpath('//ul[@id="js-live-list"]/li')

    for li in li_list:
        item = {}
        item['author'] = li.find_element_by_xpath('./span/span/i[@class="nick"]').text
        item['room_name'] = li.find_element_by_xpath('./a[@class="title new-clickstat"]').text
        item['room_cate'] = li.find_element_by_xpath('.//span/a').text
        item['watch_num'] = li.find_element_by_xpath('.//span/i[@class="js-num"]').text
        print(item)
        content_list.append(item)
        with open('huya.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(content_list, ensure_ascii=False, indent=2))
        # next_url = driver.find_elements_by_xpath('//a[@class="laypage_next"]')[0]
        # while next_url is not None:
        #     next_url.click()
        #     time.sleep(5)
        #     run()
    #time.sleep(5)
    # driver.quit()
run()