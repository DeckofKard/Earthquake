import pandas as pd
import geopandas as gpd
from fiona.crs import from_epsg
import shapely.geometry
import matplotlib.pyplot as plt
import time
import pickle
import numpy as np
import json

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
    
    gdf_pt4326 = gpd.GeoDataFrame(sido_gdf, geometry=sido_gdf['geometry'], crs=from_epsg(4326))

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

def init_sigungu_in_sido():
    #어느 행정구역인지 부여하기
    #1. 일단 시군구 별로 어느 시도인지 먼저 확인해서 sigungu_gdf에 상위 도 기록
    #이후 point별로 계산 진행
    #2-1. 어느 시도안에 있는 지 먼저 계산
    #2-2. 해당 시도 안의 시군구에게 하나씩 pip 진행해서 기록

    n = 0
    sigun_top_list = []
    for sigun_polygon in sigungu_gdf['geometry']:
        n+=1
        find_sido = False
        minx, miny, maxx, maxy = sigun_polygon.bounds
        
        
        while 1: #해당 시군구 내 대표 좌표 생성
            try:
                if sigun_polygon.contains(sigun_polygon.centroid):
                    sigun_point = sigun_polygon.centroid
                    break
                
                sigun_point = shapely.geometry.Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
                
                if sigun_polygon.contains(sigun_point):
                    break
            except:
                print("에러")
            
        for i in range(len(sido_gdf)):
            try:
                if (sido_gdf['geometry'][i]).contains(sigun_point):
                    sigun_top_list.append(sido_gdf['CTP_KOR_NM'][i])
                    print(n,sigun_point.y,sigun_point.x, sido_gdf['CTP_KOR_NM'][i])
                    find_sido = True
                    break
            except:
                print(n, "Error 발생")
                continue
        if not find_sido:
            sigun_top_list.append(None)
            print(n, sigun_point.y, sigun_point.x, "찾기 실패")

    sigungu_gdf["CTP_KOR_NM"] = sigun_top_list

    with open('./json_file/SIGUNGU_2302.json','r',encoding="utf-8") as f:
        json_data = json.load(f)

    for i,top_sido in enumerate(sigun_top_list):
        json_data["features"][i]["properties"]["CTP_KOR_NM"] = top_sido

    with open('./json_file/SIGUNGU_2302_add.json','w',encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False)


vs30_gdf = get_vs30_gdf()
sigungu_gdf = get_sigungu_gdf() #250개
sido_gdf = get_sido_gdf() #17개

#p = sido_gdf['geometry'].unary_union

#korea_polygon.bounds

try:
    with open('vs30_data/point_tf.pickle','rb') as f:
        point_tf = pickle.load(f)
except FileNotFoundError:
    korea_polygon = gpd.GeoSeries(sido_gdf.buffer(0.001).unary_union, crs=from_epsg(4326)) #위경도 0.001로 주위 보간

    point_tf = init_point_in_korea() #초기 - 3.7시간 소요
    
#vs30_korea_gdf = vs30_gdf[point_tf] #쓸모 없어짐 ㅋㅋㅋ

vs30_mapping_gdf = gpd.sjoin(vs30_gdf, sigungu_gdf) #각 점에 행정단위 매칭

for i in range(len(sigungu_gdf)): #시군구별 평균 구하기
    vs30_avg = vs30_mapping_gdf[sigungu_gdf['SIG_CD'][i] == vs30_mapping_gdf['SIG_CD']]['Vs30'].mean()
    vs30_low = vs30_mapping_gdf[sigungu_gdf['SIG_CD'][i] == vs30_mapping_gdf['SIG_CD']]['Vs30'].quantile(q=0.1)

    sigungu_gdf.loc[i,"vs30_avg"] = vs30_avg
    sigungu_gdf.loc[i,"vs30_low"] = vs30_low
    
with open('merge_gdf/sigungu_gdf_vs30.pickle', 'wb') as f:
        pickle.dump(sigungu_gdf, f)
    
#for i in range(len(sigungu_gdf)): #시군구 별로 매치
#    minx, miny, maxx, maxy = sigungu_gdf["geometry"][i].bounds

#    mask = vs30_korea_gdf.query(f'geometry.x >= {minx} & geometry.x <= {maxx} & geometry.y >= {miny} & geometry.y <= {maxy}').index
    #해당 구의 최대 범위 내에 있는 점만 뽑기
    
    
#    for m in mask: #내부 점 비교
#        try:
#            if (sigungu_gdf.loc[i,'geometry']).contains(vs30_korea_gdf.loc[m, 'geometry']): #
#                vs30_korea_gdf.loc[m, 'Top_city'] = sigungu_gdf.loc[i,'CTP_KOR_NM']
#                vs30_korea_gdf.loc[m, 'city'] = sigungu_gdf.loc[i,'SIG_KOR_NM']

#                print(m)
#        except:
#            print(m, "Error 발생")
#            continue

#    print(i, "- 완료")



#r = gpd.overlay(vs30_gdf, p, how='intersection')

fig, ax = plt.subplots(1, 2, figsize=(5, 5))
#sido_gdf.plot(ax=ax, color='lightgray', edgecolor='white')
#sigungu_gdf.plot(ax=ax, color='lightgray', edgecolor='white')

#vs30 평균값, 최하 10%값
sigungu_gdf.plot(column='vs30_avg', vmin=100, vmax=700,cmap='RdYlBu', linewidth=0.1, ax=ax[0], edgecolor='white', legend=True)
sido_gdf.plot(ax=ax[0], color=None, facecolor='none', edgecolor='lightgray',linewidth=0.8,alpha=0.8)

sigungu_gdf.plot(column='vs30_low', vmin=100, vmax=700,cmap='RdYlBu', linewidth=0.1, ax=ax[1], edgecolor='white', legend=True)
sido_gdf.plot(ax=ax[1], color=None, facecolor='none', edgecolor='lightgray',linewidth=0.8,alpha=0.8)
#vs30_korea_gdf.plot(ax=ax, color='green')

#vs30_korea_gdf.query('geometry.x > 128 & geometry.x < 129 & geometry.y > 37 & geometry.y < 38').plot(ax=ax, color='green')

#gpd.sjoin(vs30_korea_gdf, sigungu_gdf).plot(ax=ax, color='red')
#sigungu_gdf.plot(ax=ax, color='lightgray', edgecolor='white')

plt.show()

#fig.savefig("vs30.png", dpi = 500)

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

sido_gdf.plot(ax=ax, color=None, facecolor='none', edgecolor='white',linewidth=0.8)

sigungu_gdf.plot(ax=ax, color='lightgray', edgecolor='white', linewidth=0.3)

vs30_mapping_gdf.query("CTP_KOR_NM == '서울특별시'").plot(column='Vs30',ax=ax, vmin=100, vmax=700,cmap='RdYlBu') #Vs30<300
plt.show()

#fig.savefig("vs30_point.png", dpi = 500)

xlength = 7.5/901
ylength = 5.5/661

vs30_range_gdf = vs30_mapping_gdf.query("CTP_KOR_NM == '서울특별시' | CTP_KOR_NM == '경기도' | CTP_KOR_NM == '인천광역시'")

import folium
import branca.colormap as cm
colormap = cm.linear.RdYlBu_03.scale(100,700)#cm.colormap.LinearColormap(['red', 'blue'], vmin=100, vmax=700)

def style_function(feature):
    color = 'green'  # Example: Set a default color
    #if 'property_name' in feature['properties']:
        #property_value = feature['properties']['property_name']
        # Define color based on the property value

    property_value = vs30_range_gdf['Vs30'].iloc[int(feature['id'])]
    color = colormap(property_value)
    
    return {
        'fillColor': color,
        'color': color,
        'weight': 1,
        'fillOpacity': 0.5,
    }

polygons = [shapely.geometry.Polygon([(x, y), (x+xlength, y), (x+xlength, y+ylength), (x, y+ylength)]) for x, y in zip(vs30_range_gdf["geometry"].x, vs30_range_gdf["geometry"].y)]
grid_layer = gpd.GeoDataFrame(geometry=polygons, crs=from_epsg(4326))


map_center = [37.7749, 128.4194]
zoom_level = 10
m = folium.Map(location=map_center, zoom_start=zoom_level)

grid_geojson = grid_layer.to_json()
folium.GeoJson(grid_geojson, style_function=style_function).add_to(m)

folium.Choropleth(
    geo_data=sido_gdf,
    fill_color='gray',
    fill_opacity=0,
    line_opacity=0.5
    ).add_to(m)


m.save('./test.html')
