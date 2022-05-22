from matplotlib import category
import requests
from bs4 import BeautifulSoup as BS
import warnings

warnings.filterwarnings('ignore')
import os, sys

sys.path.append(os.getcwd())
import re
import tqdm
from comments.category import Category, MovieCategoryAcquirer


class SummaryAcquirer:
    def __init__(self, category_obj):
        self.catgory_obj = category_obj
        hello = category_obj.type_id
        self.film_page_url = f"https://movie.douban.com/j/chart/top_list?type={hello}&interval_id=100%3A90&action=&start=0&limit=20"
        self.resp = requests.get(self.film_page_url, headers={"User-Agent": "Mozilla/5.0"})
        self.resp.encoding = "utf-8"  # 确定解码语言，不然中文会乱码

    def get_summary(self):
        url_list = []
        for i in self.resp.json():
            url_list.append(i["url"])
        self.dic = {}
        for url in tqdm.tqdm(url_list[:10]):
            try:
                resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                hello = BS(resp.text, "html.parser")
                self.summary = hello.find("span", property="v:summary").text.strip()
                self.name = re.findall(r">(.*?)的剧情简介</", resp.text)[0]
                self.dic[self.name] = self.summary
            except AttributeError:
                print(f'Error Occured Once! ')
        return self.dic  # 得到了每个类型的大约20部电影的summary list


if __name__ == '__main__':
    cat_list = MovieCategoryAcquirer().acquire_category()
    category_obj = cat_list[0]
    s = SummaryAcquirer(category_obj)
    print(s.get_summary())
