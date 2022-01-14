#Importação das Biliotecas.

import geopandas as gpd
import fiona
import matplotlib.pyplot as plt


# Leitura do shp de focos de 2019 de incêndio no estado do RJ baixados do BDqueimadas/INPE(https://queimadas.dgi.inpe.br/queimadas/bdqueimadas/).
# Leitura do shp de Unidades de Conservação baixado do GeoPortal Inea(https://www.arcgis.com/apps/MapSeries/index.html?appid=00cc256c620a4393b3d04d2c34acd9ed).
focos_2019 = gpd.read_file('Focos_2019-01-01_2019-12-31.shp')
Ucs = gpd.read_file('gpl_ucs_estaduais_dez20.shp')

# Conversão dos limites das UCS e dos focos para coordenadas geográficas com datun wgs84.
Ucs = Ucs.to_crs("EPSG:4326")
focos = focos_2019.to_crs("EPSG:4326")

#Define função que:
# 1 - gera o plot e salva em png os focos por UC  
# 2 - salva os limites da Uc e os focos no formato kml. 

def PlotSaveFocosUc(Ucs, focos):
  for i in Ucs.index:
    Uc = Ucs[Ucs.index == i]# Define a UC.
    foco_uc = gpd.overlay(focos, Uc, how='intersection', keep_geom_type=False)# Faz a intercessão dos focos com a UC.
    if foco_uc.empty == True:
      print(f'A UC {Uc.rotulo[i]} não possui focos dentro dos seus limites')# Se o resultado da intercessão for vazio printa a msg padrão com o nome da Uc.
    else:                                                                   
      #Plota e salva o plot no formato .png
      ax = Uc.plot(color='white', edgecolor='k')
      foco_uc.plot(ax=ax, marker='x', color='red', markersize=5)
      plt.title(f'{Ucs.rotulo[i]} - Quantidade de focos:{len(foco_uc)}')
      plt.savefig(f'{Ucs.rotulo[i]}_focos_2019.png')
      plt.rcParams.update({'figure.max_open_warning': 0})
      
      # Salva no formato kml apenas os limites da Uc iterada e os focos que fazem intersecção com ela.
      fiona.supported_drivers['KML'] = 'rw'
      gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
      Uc.to_file(f'{Ucs.rotulo[i]}_limite.kml', driver='KML')
      foco_uc.to_file(f'{Ucs.rotulo[i]}_focos_2019.kml', driver='KML')
