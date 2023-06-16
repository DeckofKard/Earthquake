import pandas as pd
import json
import geopandas as gpd
from fiona.crs import from_epsg
sigungu_geojson = 'json_file/SIGUNGU_2302.json'
dfML = pd.read_csv("csv_file\\earthquake_ML.csv")
dfML = dfML.drop(['Unnamed: 0'], axis= 'columns')

with open(sigungu_geojson,'r',encoding="utf-8") as f:
    json_data = json.load(f)

gdf_pt_geom = gpd.points_from_xy(dfML.long, dfML.lat)
eq_gpd = gpd.GeoDataFrame(dfML, geometry=gdf_pt_geom, crs=from_epsg(4326))              # dfML 좌표


sigungu_gdf = gpd.read_file(sigungu_geojson)
sigungu_gdf = gpd.GeoDataFrame(sigungu_gdf, geometry=sigungu_gdf['geometry'], crs=from_epsg(4326))          # 시군구 geodataframe

place_data = gpd.sjoin(eq_gpd, sigungu_gdf, how = "inner")
for i in range(len(sigungu_gdf)): #시군구별 평균 구하기
    ml_erg = place_data[sigungu_gdf['SIG_CD'][i] == place_data['SIG_CD']]['ml_erg'].sum() / 1000
    ml_max = place_data[sigungu_gdf['SIG_CD'][i] == place_data['SIG_CD']]['ml'].max()

    sigungu_gdf.loc[i,"ml_erg"] = ml_erg
    sigungu_gdf.loc[i,"ml_max"] = ml_max

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

sigungu_gdf.plot(column='ml_max',cmap='RdYlBu', ax=ax, edgecolor='white', linewidth=0.3)

eq_gpd.plot(ax=ax, color='green')
place_data.plot(ax=ax, color='red')
plt.show()
