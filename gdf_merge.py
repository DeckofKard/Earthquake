import pandas as pd
import geopandas as gpd
from fiona.crs import from_epsg
import shapely.geometry
import matplotlib.pyplot as plt
import time
import pickle
import numpy as np
import json

with open('merge_gdf/sigungu_gdf_vs30.pickle','rb') as f: #vs30
    sigungu_gdf_vs30 = pickle.load(f)

with open('merge_gdf/sigungu_gdf_shelav.pickle','rb') as f: #수용인구 수
    sigungu_gdf_shelav = pickle.load(f)

population_df = pd.read_csv("csv_file/population.csv") #인구 수
population_df["code"] = population_df["code"].astype(str)

Seismic_design_ratio_df = pd.read_csv("csv_file/Seismic_design_ratio.csv") #내진 비율

#대피소 수용율(인구수 / 내진 비율 계산)
sigungu_gdf = pd.concat([sigungu_gdf_vs30, sigungu_gdf_shelav["shel_av"]] , axis=1)
sigungu_gdf = pd.merge(sigungu_gdf, population_df[["code", "2023년05월_총인구수"]] , left_on="SIG_CD", right_on = "code", how="left").drop(["code"],axis=1)
for i in range(len(sigungu_gdf)):
    sigungu_gdf.loc[i,"2023년05월_총인구수"] = int(sigungu_gdf["2023년05월_총인구수"][i].replace(",",''))

sigungu_gdf['shelter_able'] = sigungu_gdf['shel_av'] / sigungu_gdf['2023년05월_총인구수'] *100

sigungu_gdf = pd.concat([sigungu_gdf, Seismic_design_ratio_df["내진설계_비율"]] , axis=1)

sigungu_gdf.to_csv("csv_file/sigungu_gdf.csv", encoding="utf-8-sig")
