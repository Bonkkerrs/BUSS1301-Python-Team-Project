import json
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
result = open("科幻片数据统计.json",'r',encoding='utf-8')
print(result)
data=json.load(result)
film_year=[]
film_score=[]
for film in data:
    if int(film['year'])>1980:
        film_year.append(int(film['year']))
        film_score.append(float(film['score']))
core=np.corrcoef(np.array(film_score),np.array(film_year))
print(core)
plt.scatter(film_year,film_score)
plt.show()