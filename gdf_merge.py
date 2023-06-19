import pandas as pd
import geopandas as gpd
from fiona.crs import from_epsg
import shapely.geometry
import matplotlib.pyplot as plt
import time
import pickle
import numpy as np
import json
import matplotlib.pyplot as plt

with open('merge_gdf/sigungu_gdf_vs30.pickle','rb') as f: #vs30
    sigungu_gdf_vs30 = pickle.load(f)

with open('merge_gdf/sigungu_gdf_shelav.pickle','rb') as f: #수용인구 수
    sigungu_gdf_shelav = pickle.load(f)

population_df = pd.read_csv("csv_file/population.csv") #인구 수
population_df["code"] = population_df["code"].astype(str)


#대피소 수용율(인구수 / 내진 비율 계산)
sigungu_gdf = pd.concat([sigungu_gdf_vs30, sigungu_gdf_shelav["shel_av"]] , axis=1)

sigungu_gdf = pd.merge(sigungu_gdf, population_df[["code", "2023년05월_총인구수"]] , left_on="SIG_CD", right_on = "code", how="left").drop(["code"],axis=1)
for i in range(len(sigungu_gdf)):
    sigungu_gdf.loc[i,"2023년05월_총인구수"] = int(sigungu_gdf["2023년05월_총인구수"][i].replace(",",''))

sigungu_gdf['shelter_able'] = sigungu_gdf['shel_av'] / sigungu_gdf['2023년05월_총인구수'] *100

plt.rcParams['font.family'] = "NanumSquare"
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

sigungu_gdf['shelter_able'] = sigungu_gdf['shelter_able'].astype(int)

sigungu_gdf.plot(column='shelter_able',cmap='RdYlBu',vmin=0, vmax=100, ax=ax, edgecolor='white', linewidth=0.3,legend=True)

plt.title(" 대피소 인구대비 수용 가능 비율", fontdict = {'fontsize' : 25, 'fontweight':"bold"}, pad=10)
plt.show()
#fig.savefig("대비소수용비율.png", dpi = 500)

Seismic_design_ratio_df = pd.read_csv("csv_file/Seismic_design_ratio.csv") #내진 비율
sigungu_gdf = pd.concat([sigungu_gdf, Seismic_design_ratio_df["내진설계_비율"]] , axis=1)
#내진설계 비율 시각화
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
sigungu_gdf.plot(column='내진설계_비율',cmap='RdYlBu', vmin=0, vmax=100, ax=ax, edgecolor='white', linewidth=0.3,legend=True)

plt.title("전국 시군구별 내진설계 비율", fontdict = {'fontsize' : 25, 'fontweight':"bold"}, pad=10)
plt.show()
#fig.savefig("내진설계비율.png", dpi = 500)

sigungu_gdf_sort = sigungu_gdf.query("CTP_KOR_NM == '서울특별시'").sort_values('내진설계_비율',ascending=False)
fig, ax = plt.subplots(1, 1, figsize=(10, 20))
ax.barh(sigungu_gdf_sort["SIG_KOR_NM"],sigungu_gdf_sort["내진설계_비율"], color="red")
plt.title("서울시 자치구별 내진설계 비율", fontdict = {'fontsize' : 25, 'fontweight':"bold"}, pad=10)
plt.show()
fig.savefig("mt_max_bar.png", dpi = 500)


#sigungu_gdf.to_csv("csv_file/sigungu_gdf.csv", encoding="utf-8-sig")

with open('merge_gdf/sigungu_gdf_eq.pickle','rb') as f: #수용인구 수
    sigungu_gdf_eq = pickle.load(f)
    
sigungu_gdf = pd.concat([sigungu_gdf, sigungu_gdf_eq["ml_max_new"]] , axis=1)

#위험도
eq_100 = sigungu_gdf['ml_max_new'].rank(method='max', ascending=True)/ len(sigungu_gdf) #최대규모는 높을 수록 위험 #상대점수
vs30_100 = sigungu_gdf['vs30_low'].rank(method='max', ascending=False)/ len(sigungu_gdf) #vs30은 낮을 수록 위험 #상대점수

#대비도
shelter_100 = sigungu_gdf['shelter_able'].rank(method='max', ascending=True)/ len(sigungu_gdf) #대피소 수용인원은 높을 수록 안전  #상대점수
seismic_100 = sigungu_gdf['내진설계_비율'].rank(method='max', ascending=True)/ len(sigungu_gdf) #내진설계비율은 높을 수록 안전  #상대점수


sigungu_gdf['total_danger'] = (eq_100+vs30_100) / (shelter_100 + seismic_100) #위험수치 = 위험도/대비도

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
sigungu_gdf.plot(column='total_danger',cmap='coolwarm', vmin=0, vmax=1, ax=ax, edgecolor='white', linewidth=0.3,legend=True)
plt.title("시군구별 지진 위험도/대비율 수치", fontdict = {'fontsize' : 25, 'fontweight':"bold"}, pad=10)

plt.show()
#fig.savefig("지진안전수치.png", dpi = 500)

sigungu_gdf_sort = sigungu_gdf.sort_values('total_danger',ascending=False).head(20)
fig, ax = plt.subplots(1, 1, figsize=(10, 20))
ax.barh(sigungu_gdf_sort["CTP_KOR_NM"]+" "+sigungu_gdf_sort["SIG_KOR_NM"],sigungu_gdf_sort["total_danger"], color="red")
plt.title("전국 시군구별 위험도/대비율 수치", fontdict = {'fontsize' : 25, 'fontweight':"bold"}, pad=10)
plt.show()
