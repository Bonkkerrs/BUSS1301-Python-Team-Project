import requests
import re
from lxml import etree
from wordcloud import WordCloud
import matplotlib
import jieba
import codecs
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

limit = 100
response = requests.get(f'https://movie.douban.com/subject/1292052/comments?limit={limit}&status=P&sort=new_score',
                        headers=headers)
div_list = etree.HTML(response.text).xpath('//*[@id="comments"]/div')[:limit]
content_X = []
print(div_list)
for div in div_list:
    comment = div.xpath("./div[2]/p/span/text()")[0]
    content_X.append(comment)

# 导入、分词
segment = []
for line in content_X:
    try:
        segs = jieba.lcut(line)  # jiaba.lcut()
        for seg in segs:
            if len(seg) > 1 and seg != '\r\n':
                segment.append(seg)
    except:
        print(line)
        continue

print(content_X)
# 去停用词
words_df = pd.DataFrame({'segment': segment})
stopwords = pd.read_csv("stopwords.txt"
                        , index_col=False
                        , quoting=3
                        , sep="\t"
                        , names=['stopword']
                        , encoding='utf-8')  # quoting=3 全不引用
# stopwords.head()
words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

print(words_df)
# 统计词频
words_stat = words_df.groupby(by=['segment'])['segment'].agg([("计数", "count")])
words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
# words_stat.head()

# 词云
wordcloud = WordCloud(font_path="simhei.ttf"
                      , background_color="white"
                      , max_font_size=80)
word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}
wordcloud = wordcloud.fit_words(word_frequence)
plt.imshow(wordcloud)
plt.show()
