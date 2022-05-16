import requests
from lxml import etree
from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt
import pandas as pd


class MovieCommentCrawler:
    def __init__(self, id, limit=50):
        self.id = id
        self.limit = limit
        self.content_X = self.crawl_comments()
        self.segment = self.segment_words()
        self.words_df = self.get_words_df()
        self.words_stat = self.get_words_stat()

    def crawl_comments(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        limit = self.limit
        response = requests.get(
            f'https://movie.douban.com/subject/{self.id}/comments?limit={limit}&status=P&sort=new_score',
            headers=headers)
        div_list = etree.HTML(response.text).xpath('//*[@id="comments"]/div')[:limit]
        content_X = []
        for div in div_list:
            comment = div.xpath("./div[2]/p/span/text()")[0]
            content_X.append(comment)
        return content_X

    def segment_words(self):
        segment = []
        for line in self.content_X:
            try:
                segs = jieba.lcut(line)
                for seg in segs:
                    if len(seg) > 1 and seg != '\r\n':
                        segment.append(seg)
            except:
                print(line)
                continue
        return segment

    def get_words_df(self):
        words_df = pd.DataFrame({'segment': self.segment})
        stopwords = pd.read_csv("stopwords.txt",
                                index_col=False,
                                quoting=3,
                                sep="\t",
                                names=['stopword'],
                                encoding='utf-8')
        words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
        return words_df

    def get_words_stat(self):
        words_stat = self.words_df.groupby(by=['segment'])['segment'].agg([("计数", "count")])
        words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
        return words_stat

    def generate_wordcloud(self):
        fig = plt.figure(dpi=600)
        wordcloud = WordCloud(font_path="simhei.ttf",
                              max_font_size=80,
                              width=600, height=400,
                              scale=4
                              )
        word_frequence = {x[0]: x[1] for x in self.words_stat.head(1000).values}
        wordcloud = wordcloud.fit_words(word_frequence)
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()
        return fig


if __name__ == '__main__':
    m = MovieCommentCrawler(id='35613853', limit=100)
    m.generate_wordcloud()
