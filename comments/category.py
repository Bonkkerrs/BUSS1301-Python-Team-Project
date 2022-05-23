import json
import requests
import re
from lxml import etree


class Category:
    def __init__(self, type_name, type_id):
        self.type_name = type_name
        self.type_id = type_id

    def __str__(self):
        return self.type_name

    def query_list(self, ranking_limit):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        url = f'https://movie.douban.com/j/chart/top_list?type={self.type_id}&interval_id=100:90&action=&start=0&limit={ranking_limit}'
        print(url)
        response = requests.get(url, headers=headers)
        print(response)
        return json.loads(response.text)

    def get_category_dict(self):
        return {
            self.type_name: f'https://movie.douban.com/j/chart/top_list?type={self.type_id}&interval_id=100%3A90&action=&start=0&limit=20'}


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
    print(c.get_category_dict())
    c.query_list(10)
