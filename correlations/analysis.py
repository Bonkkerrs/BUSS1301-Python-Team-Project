import json
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import os, sys

sys.path.append(os.getcwd())
from comments.ranking import RankingCrawler
from comments.category import MovieCategoryAcquirer


class CorrelationAnalyzer:
    def __init__(self, category_obj, query_limit):
        self.film_type = category_obj.type_name
        r = RankingCrawler(category_obj, query_limit)
        self.film_length = r.get_length_list()
        self.film_year = [int(movie.get_year()) for movie in r.movie_list]
        self.film_score = [float(movie.score) for movie in r.movie_list]
        print(self.film_length, self.film_year, self.film_score)

    def length_year(self):
        core = np.corrcoef(np.array(self.film_year),
                           np.array(self.film_length))
        print(core)
        plt.scatter(self.film_length, self.film_year)
        plt.show()

    def length_score(self):
        core = np.corrcoef(np.array(self.film_score),
                           np.array(self.film_length))
        print(core)
        plt.scatter(self.film_score, self.film_year)
        plt.show()

    def score_year(self):
        core = np.corrcoef(np.array(self.film_year), np.array(self.film_score))
        print(core)
        plt.scatter(self.film_score, self.film_year)
        plt.show()


if __name__ == '__main__':
    cat_list = MovieCategoryAcquirer().acquire_category()
    category_obj = cat_list[0]
    c = CorrelationAnalyzer(category_obj, 50)
    c.score_year()
    c.length_score()
    c.length_year()
