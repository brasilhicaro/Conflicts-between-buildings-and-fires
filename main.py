import osmnx as ox
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt

place_name = "Patos, Brazil"

# Obtenha os polígonos dos edifícios
geometries = ox.geometries_from_place(place_name, tags={"building": True, "residential": True})

# Crie um GeoDataFrame a partir dos polígonos dos edifícios
gdf_predios = gpd.GeoDataFrame(geometries)

coordenadas = [(-7.0171, -37.2754), (-7.0225, -37.2822), (-7.0156, -37.2678), (-7.0171, -37.2754), (-6.9938, -37.2667)]

# Cria lista de pontos
pontos = [Point(lon, lat) for lat, lon in coordenadas]

# Define a distância de verificação
distancia_limite = 0.001

# Inicialize um GeoDataFrame vazio para armazenar os pontos próximos aos edifícios
pontos_proximos = gpd.GeoDataFrame(columns=['geometry'])

# Itera os pontos e verifique se estão perto de algum edifício
for ponto in pontos:
    perto_de_predios = gdf_predios[gdf_predios.geometry.distance(ponto) < distancia_limite]
    if not perto_de_predios.empty:
        novo_ponto = gpd.GeoDataFrame({'geometry': [ponto]}, geometry='geometry')
        pontos_proximos = pd.concat([pontos_proximos, novo_ponto], ignore_index=True)

# Visualize os resultados
fig, ax = plt.subplots()
gdf_predios.plot(ax=ax, alpha=0.7)
pontos_proximos.plot(ax=ax, color='blue', marker='o', markersize=50)

# Desenhe círculos representando a área ao redor de cada ponto
for ponto in pontos:
    circle = ponto.buffer(distancia_limite)
    gpd.GeoSeries(circle).plot(ax=ax, color='red', alpha=0.2)

# Marque os pontos originais em verde
pontos_gdf = gpd.GeoDataFrame(geometry=pontos)
pontos_gdf.plot(ax=ax, color='green', marker='*', markersize=100)

# Exiba uma mensagem indicando se há edifícios/casas próximos para cada ponto
for index, ponto in pontos_proximos.iterrows():
    plt.text(ponto['geometry'].x, ponto['geometry'].y, 'Há edifícios/casas próximos!', color='red', fontsize=12)

plt.show()
