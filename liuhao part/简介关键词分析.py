import json
import requests
import re
from lxml import etree
from bs4 import BeautifulSoup as BS
import warnings
warnings.filterwarnings("ignore")
import jieba   # 分词包
from jieba import analyse
import numpy as np
import codecs
import pandas as pd

class Category:
    def __init__(self, type_name, type_id):
        self.type_name = type_name
        self.type_id = type_id

    def query_list(self, ranking_limit):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        url = f'https://movie.douban.com/j/chart/top_list?type={self.type_id}&interval_id=100:90&action=&start=0&limit={ranking_limit}'
        response = requests.get(url, headers=headers)
        return json.loads(response.text)


class MovieCategoryAcquirer:
    def __init__(self):
        self.category_list = self.acquire_category()

    def acquire_category(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        response = requests.get('https://movie.douban.com/chart', headers=headers)
        span_list = etree.HTML(response.text).xpath('//*[@id="content"]/div/div[2]/div[1]/div/span')
        category_list = []
        for span in span_list:
            type_href = span.xpath('./a')[0].xpath('./@href')[0]
            type_name = span.xpath('./a')[0].text
            type_id = self.parse_category(type_href)
            c = Category(type_name, type_id)
            category_list.append(c)
        return category_list

    @staticmethod
    def parse_category(href):
        try:
            type_id = re.findall('&type=(.*?)&', href)[0]
            return type_id
        except IndexError:
            print("地址解析失败！")
            return None


if __name__ == '__main__':
    # m = MovieCategoryAcquirer()
    c = Category("剧情", '11')
    c.query_list(10)




###########################################################################################建立一个字典方便查询
m = MovieCategoryAcquirer()
cat_list = m.acquire_category()
type_number={}
for cat in cat_list:
    type_number[cat.type_name]= cat.type_id
#爬取每个分类里的电影
class Get_summary:
    def __init__(self,type):
        self.type=type
        hello=type_number[self.type]
        self.film_page_url = f"https://movie.douban.com/j/chart/top_list?type={hello}&interval_id=100%3A90&action=&start=0&limit=20"
        self.resp = requests.get(self.film_page_url, headers={"User-Agent": "Mozilla/5.0"})
        self.resp.encoding = "utf-8"  # 确定解码语言，不然中文会乱码
    def get_summary(self):
        url=[]
        for i in self.resp.json():
            url.append(i["url"])
        self.dic={}
        i=0
        while i<=4:
            resp=requests.get(url[i], headers={"User-Agent": "Mozilla/5.0"})
            hello=BS(resp.text,"html.parser")
            self.summary=hello.find("span",property="v:summary").text.strip()
            self.name=re.findall(r">(.*?)的剧情简介</",resp.text)[0]
            self.dic[self.name]=self.summary
            i+=1
        return self.dic #得到了每个类型的大约20部电影的summary list
#制作停用词表
with open(r"停用词表.txt", encoding='utf-8') as f:
    kk = f.readlines()
    content = []
    for i in kk:
        content.append(i.strip())
    f.close()
#分析数据
class Analyse:
    def __init__(self,every_summary):
        global content
        self.every_summary=every_summary
    #清洗数据
    def handle_word(self):
        hello=[]
        #分词
        for m in self.every_summary.values():
            after_cut = jieba.lcut(m,cut_all=False)
            #去停用词
            for i in set(after_cut):
                if re.match(r'\w+', i) and i not in content:
                    hello.append(i)
        return hello
    #关键词分析
    def text_rank(self):
        for m,n in zip(self.every_summary.keys(),self.every_summary.values()):
            self.keywords = analyse.textrank(n,
                                        topK=10,
                                        withWeight=False,
                                        allowPOS=('ns', 'n', 'vn', 'n'))
            print(m,self.keywords)
        return self.keywords
juqing=Get_summary('剧情').get_summary()
m=Analyse(juqing)
m.text_rank()






