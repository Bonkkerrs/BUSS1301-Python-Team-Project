import json
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
result = open("喜剧片数据统计.json",'r',encoding='utf-8')
print(result)
data=json.load(result)
film_length=[]
film_year=[]
for film in data:
    if int(film['length'])>70:
        film_length.append(int(film['length']))
        film_year.append(float(film['year']))
core=np.corrcoef(np.array(film_year),np.array(film_length))
print(core)
plt.scatter(film_length,film_year)
plt.show()