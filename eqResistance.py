import folium
import json

city_data = {

    'Seoul': 0.20,
    'Busan': 0.12,
    'Daegu': 0.155,
    'Incheon': 0.201,
    'Gwangju': 0.183,
    'Daejeon': 0.196,
    'Ulsan': 0.214,
    'Gyeonggi-do': 0.247,
    'Gangwon-do': 0.124,
    'Chungcheongbuk-do': 0.142,
    'Chungcheongnam-do': 0.144,
    'Jeollabuk-do': 0.133,
    'Jeollanam-do': 0.102,
    'Gyeongsangbuk-do': 0.113,
    'Gyeongsangnam-do': 0.121,
    'Jeju': 0.174
}


geojson_file = "json_file\\skorea-provinces-geo.json"


with open(geojson_file, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)


center = [36.5, 127.5]

folium 
map = folium.Map(location=center, zoom_start=7)



all_provinces = []  # 모든 지역을 저장하기 위한 리스트

for feature in geojson_data['features']:
    properties = feature['properties']
    province = properties['NAME_1']
    all_provinces.append(province)  # 모든 지역을 리스트에 추가
    
    if province in city_data:
        rate = city_data[province]
        color = 'blue'
        
        if rate <= 0.1:
            color = 'red'
        elif rate <= 0.15:
            color = 'orange'
        elif rate <= 0.2:
            color = 'yellow'
       
        folium.GeoJson(
            feature,
            style_function=lambda x, color=color: {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            }
        ).add_to(map)

'''
# 모든 지역 출력
for province in all_provinces:
    print(province)
'''
# 지도를 HTML 파일로 저장
map.save('earthquake_map.html')



# 내진율에 따라 구역별로 색상 설정
for feature in geojson_data['features']:
    properties = feature['properties']
    province = properties['NAME_1']
 
    # 내진율 데이터가 있는 경우에만 색상 설정
    if province in city_data:
        rate = city_data[province]
        if rate <= 0.1:
            color = 'red'
        elif rate <= 0.15:
            color = 'orange'
        elif rate <= 0.2:
            color = 'yellow'
        else:
            color = 'green'

        folium.GeoJson(
            feature,
            style_function=lambda x: {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            }
        ).add_to(map)