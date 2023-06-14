import pandas as pd
import geopandas as gpd
from fiona.crs import from_epsg
import shapely.geometry
import matplotlib.pyplot as plt
import time
import pickle

def get_vs30_gdf(): #pickle 대체 대비 함수화
    vs30_df = pd.read_csv("vs30_data/figure17b.dat", sep = '\t') #dat 파일 입력
    #위도 내림차순 1순위 정렬, 경도 오름차순 2순위 정렬 기본

    #vs30_df = vs30_df.sort_values(by=['longitude','latitude']) #위'latitude' 경도'longitude'기준으로 올림차순 정렬 <- 하니까 괜히 틀어짐
    gdf_pt_geom = gpd.points_from_xy(vs30_df.longitude, vs30_df.latitude) #위경도 숫자를 포인트(좌표)로 변환

    gdf_pt4326 = gpd.GeoDataFrame(vs30_df["Vs30"], geometry=gdf_pt_geom, crs=from_epsg(4326)) #DataFrame화(좌표 4326-위경도)
    #위경도 숫자로 된 열 버리고 Vs30이랑 Point(경도, 위도)만 있음
    
    return gdf_pt4326

def get_sigungu_gdf():
    sigungu_geojson = 'json_file/SIGUNGU_2302.json'
    sigungu_gdf = gpd.read_file(sigungu_geojson)
    
    gdf_pt4326 = gpd.GeoDataFrame(sigungu_gdf, geometry=sigungu_gdf['geometry'], crs=from_epsg(4326))

    return gdf_pt4326

def get_sido_gdf():
    sido_geojson = 'json_file/SIDO_2302.json'
    sido_gdf = gpd.read_file(sido_geojson)
    
    gdf_pt4326 = gpd.GeoDataFrame(sigungu_gdf, geometry=sigungu_gdf['geometry'], crs=from_epsg(4326))

    return gdf_pt4326

def init_point_in_korea():
    i = 0
    point_tf = []
    st = time.time()
    for p in vs30_gdf['geometry']:
        point_tf.append((p.within(korea_polygon))[0])
        i+=1
        print(i)
        
    ft = time.time()
    print(ft-st)
    with open('point_tf.pickle', 'wb') as f:
        pickle.dump(point_tf, f)

    return point_tf


vs30_gdf = get_vs30_gdf()
sigungu_gdf = get_sigungu_gdf()
sido_gdf = get_sido_gdf()

korea_polygon = gpd.GeoSeries(sido_gdf.buffer(0.001).unary_union, crs=from_epsg(4326)) #위경도 0.001로 주위 보간
#p = sido_gdf['geometry'].unary_union

#korea_polygon.bounds

try:
    with open('vs30_data/point_tf.pickle','rb') as f:
        point_tf = pickle.load(f)
except FileNotFoundError:
    point_tf = init_point_in_korea() #초기 - 3.7시간 소요
    
vs30_korea_gdf = vs30_gdf[point_tf]

#r = gpd.overlay(vs30_gdf, p, how='intersection')

fig, ax = plt.subplots(1, 1, figsize=(5, 5))
#sido_gdf.plot(ax=ax, color='lightgray', edgecolor='white');
korea_polygon.plot(ax=ax, color='lightgray', edgecolor='white')
vs30_korea_gdf.plot(ax=ax, color='green')

plt.show()
