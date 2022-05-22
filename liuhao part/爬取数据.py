import json

import selenium, time, re

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common import keys

web_source = {
    '剧情片': 'https://movie.douban.com/tag/#/?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E5%89%A7%E6%83%85',
    '喜剧片': 'https://movie.douban.com/tag/#/?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E5%96%9C%E5%89%A7',
    '科幻片': 'https://movie.douban.com/tag/#/?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E7%A7%91%E5%B9%BB'
}


def get_data(x):
    # 设置四个列表
    film = []
    # 1.创建浏览器对象
    web = Chrome()
    # 2.打开一个网址
    film_type = web_source[x]
    web.get(film_type)
    time.sleep(1)
    for i in range(1, 6):
        web.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/a').click()
        time.sleep(1)
    f = open(f"{x}数据统计.json", mode='w', encoding="utf-8")
    for t in range(1, 101):
        dic = {}
        web.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div/div[1]/div/div/div[1]/div[3]/a[{t}]').click()
        # 切换窗口至倒数第一个页面（即最新）
        web.switch_to.window(web.window_handles[-1])
        # 查找评分
        score = web.find_element(By.XPATH, '//*[@id="interest_sectl"]/div[1]/div[2]/strong').text

        # 查找年份
        year_ = web.find_element(By.XPATH, '//*[@id="content"]/h1/span[2]').text
        year = year_[1:-1]
        # 查找片长
        length_ = web.find_element(By.XPATH, '//*[@id="info"]').text
        try:
            length = re.findall(r"(\d+?)分钟", length_)[0]
            # 查找名字
            name = web.find_element(By.XPATH, '//*[@id="content"]/h1/span[1]').text
            # 加载dic
            dic['name'] = name
            dic['year'] = year
            dic['length'] = length
            dic['score'] = score
            film.append(dic)
            print(t)
            web.close()
            web.switch_to.window(web.window_handles[0])
        except IndexError:
            web.close()
            web.switch_to.window(web.window_handles[0])
    list_json = json.dumps(film, ensure_ascii=False)
    f.write(list_json)
    f.close()


get_data('剧情片')
get_data('喜剧片')
get_data('科幻片')
