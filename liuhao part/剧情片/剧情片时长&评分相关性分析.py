import json
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
result = open("剧情片数据统计.json",'r',encoding='utf-8')
print(result)
data=json.load(result)
film_length=[]
film_score=[]
for film in data:
    if int(film['length'])>70:
        film_length.append(int(film['length']))
        film_score.append(float(film['score']))
core=np.corrcoef(np.array(film_score),np.array(film_length))
print(core)
plt.scatter(film_length,film_score)
plt.show()