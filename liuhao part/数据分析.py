import json
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
class Ana:
    def __init__(self,film_type):
        self.film_type=film_type
        result = open(f"{self.film_type}数据统计.json", 'r', encoding='utf-8')
        data = json.load(result)
        self.film_length = []
        self.film_year = []
        self.film_score = []
        for film in data:
            if int(film['length']) > 70:
                self.film_length.append(int(film['length']))
                self.film_year.append(float(film['year']))
                self.film_score.append(float(film['score']))
    def length_year(self):
        core = np.corrcoef(np.array(self.film_year), np.array(self.film_length))
        print(core)
        plt.scatter(self.film_length, self.film_year)
        plt.show()
    def length_score(self):
        core = np.corrcoef(np.array(self.film_score), np.array(self.film_length))
        print(core)
        plt.scatter(self.film_score, self.film_year)
        plt.show()
    def score_year(self):
        core = np.corrcoef(np.array(self.film_year), np.array(self.film_score))
        print(core)
        plt.scatter(self.film_score, self.film_year)
        plt.show()
a1=Ana('喜剧片')
a1.score_year()






