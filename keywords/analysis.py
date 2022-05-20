import jieba
import os, sys
sys.path.append(os.getcwd())
from summary import SummaryAcquirer
from comments.category import MovieCategoryAcquirer
from jieba import analyse


class KeywordsAnalyzer:
    def __init__(self, every_summary):
        global content
        self.every_summary = every_summary

    # 清洗数据
    def handle_word(self):
        hello = []
        # 分词
        for m in self.every_summary.values():
            after_cut = jieba.lcut(m, cut_all=False)
            # 去停用词
            for i in set(after_cut):
                if re.match(r'\w+', i) and i not in content:
                    hello.append(i)
        return hello

    # 关键词分析
    def text_rank(self):
        for m, n in zip(self.every_summary.keys(), self.every_summary.values()):
            self.keywords = analyse.textrank(n,
                                             topK=10,
                                             withWeight=False,
                                             allowPOS=('ns', 'n', 'vn', 'n'))
            print(m, self.keywords)
        return self.keywords


if __name__ == '__main__':
    cat_list = MovieCategoryAcquirer().acquire_category()
    category_obj = cat_list[0]
    s = SummaryAcquirer(category_obj)
    k = KeywordsAnalyzer(s.get_summary())
    kewords_dict = k.text_rank()
    