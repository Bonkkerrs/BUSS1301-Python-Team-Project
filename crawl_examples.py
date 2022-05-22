import re
from urllib import response
import requests
from lxml import etree
from tqdm import tqdm


class Project:
    def __init__(self, title, report, demo):
        self.title = title.split('by')[0].strip()
        self.report_url = report
        self.demo_url = demo
        self.download(title + '.pdf', self.report_url)
        # self.download(title + '.mp4', self.demo_url)

    @staticmethod
    def download(fname, url):
        file = requests.get(url).content
        with open(f'./Examples/{fname}', 'wb+') as fp:
            fp.write(file)


if __name__ == '__main__':
    p_list = []
    base_html = 'http://yangbao.org/'
    target = 'http://yangbao.org/notes/2020/07/09/cs159-2020-student-projects'
    response = requests.get(target)
    div = etree.HTML(response.text).xpath('/html/body/div/div[2]/div/div[1]')[0]
    ul_list = div.xpath('./ul')
    li_list = []
    for ul in ul_list:
        li_list += ul.xpath('./li')

    for li in tqdm(li_list):
        title = li.text
        html_list = li.xpath('./ul/li/a')
        report = base_html + html_list[0].xpath('./@href')[0]
        demo = base_html + html_list[1].xpath('./@href')[0]
        p = Project(title, report, demo)
        p_list.append(p)
