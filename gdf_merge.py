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


Seismic_design_ratio = pd.read_csv("csv_file/Seismic_design_ratio.csv") #내진 비율

sigungu_gdf = pd.concat([sigungu_gdf_vs30, sigungu_gdf_shelav["shel_av"]] , axis=1)
sigungu_gdf = pd.concat([sigungu_gdf, Seismic_design_ratio["내진설계_비율"]] , axis=1)
