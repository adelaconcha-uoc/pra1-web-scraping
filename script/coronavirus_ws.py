#importa librerías

#importamos las librerías de BeautifulSoup para obtener el código de html y ayudarnos al scraping
#se importa de librería de request para "conectarse" a la url
from bs4 import BeautifulSoup as soup
from requests import get
#relacionadas a gestión de datos por medio de dataframes
import pandas as pd
import numpy as np
#relacionadas a base de datos (Postgres)
from sqlalchemy import create_engine
import psycopg2 
import io


#se obtiene el código html
my_url = "https://www.worldometers.info/coronavirus/"
pageHTML = get(my_url)
soup = soup(pageHTML.text)

# con este código obtenemos la tabla que contiene la información de detalle de país que es la que queremos obtener.
# previo a escribir este código, se hizo una búsqueda manual en la página mirando el código de html para ver
# en dónde se encontraba la información, esta revisión se hizo con el browser, utilizando las herramientas de desarrollador
# que permiten ubicar el código señalando el objeto de interés, en este caso la tabla. Para esto utilicé Chrome con las
# herramientas de desarrollador y encontré que el objeto 'table' con la etiqueta 'tbody' contenía los valoresdata = []
data = []
table = soup.find('table')
table_body = table.find('tbody')

# se van ubicando los saltos de línea para poder ir uno a uno llenando las líneas de la variable de tabla en donde 
# se guardarán los datos
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols) #quita los valores vacíos

# eliminamos los valores que no tienen datos, si es que hay alguno
missingData = []
fixedData = [[]]
for row in data:
    for index,col in enumerate(row):
        if(col == ''):
            row[index] = 0

    missingData.append(row)

# definimos las cabeceras de acuerdo a la tabla de la web, colocando el nombre que queramos para las columnas.
# debemos tener cuidado porque la página fuente es actualizada constantemente, desde que inicié la práctica, se han hecho
# 5 cambios y se añaden líneas o columnas y si las columnas no coinciden, esta parte del código debe ser revisada y ajustada
# ya que de otra forma enviará un error, la forma de evitar el error es revisar el nombre de las columnas en la página fuente
# y dejar igual las columnas en un sitio y otro, si hay columnas o líneas no útiles, más adeoante se pueden eliminar.

headers = ["Country", "Total Cases", "New Cases", "Total Deaths","New Deaths", "Total Recovered", "Active Cases", "Serious, Critical", "Tot Cases/1M pop", "Tot Deaths/1M pop", "Total Tests", "Tests/1M pop", "Region"]

# hasta este punto se ha hecho el scraping y la información está lista para pasar a un dataframe

#pasa la información a un dataframe
df = pd.DataFrame()
df = df.append(data)
df.columns = headers

## Elimina los signos que impiden convertir a número

df['Total Cases'] = df['Total Cases'].str.replace(',', '')
df['New Cases'] = df['New Cases'].str.replace('+', '')
df['New Cases'] = df['New Cases'].str.replace(',', '')
df['Total Deaths'] = df['Total Deaths'].str.replace(',', '')
df['New Deaths'] = df['New Deaths'].str.replace('+', '')
df['New Deaths'] = df['New Deaths'].str.replace(',', '')
df['Total Recovered'] = df['Total Recovered'].str.replace(',', '')
df['Active Cases'] = df['Active Cases'].str.replace(',', '')
df['Serious, Critical'] = df['Serious, Critical'].str.replace(',', '')
df['Tot Cases/1M pop'] = df['Tot Cases/1M pop'].str.replace(',', '')
df['Tot Deaths/1M pop'] = df['Tot Deaths/1M pop'].str.replace(',', '')

#caso irregular ocurrido el 13 de abril:

df['Total Recovered'] = df['Total Recovered'].str.replace('N/A', '0')

## Elimina los NaN para valores nulos y los sustituye por ceros
df.fillna(0, inplace=True)

# cambia los tipos de dato del dataframe, para poder enviar el dataframe eventualmente a una base de datos.
# en caso de enviarlo a un csv, este paso no tiene tanto impacto, sin embargo si queremos hacer operaciones con el
# dataframe, lo mejor es tener las columas declaradas en el formato correcto:

df = df.astype({"Total Cases": int})
df = df.astype({"New Cases": int})
df = df.astype({"Total Deaths": int})
df = df.astype({"New Deaths": int})
df = df.astype({"Total Recovered": int})
df = df.astype({"Active Cases": int})
df = df.astype({"Serious, Critical": int})
df = df.astype({"Tot Cases/1M pop": float})
df = df.astype({"Tot Deaths/1M pop": float})

# Removemos columnas y líneas no utilizadas
# es importante señalar que para este caso, he decidido quitar estas columnas, porque el scraping del covid está
# teniendo mucho movimiento porque al tratarse de un tema de interés mundial, la página fuente altera la tabla constantemente
# para aportar más información y en nuestra párctica no toda la información es relavante

# elimino 3 columnas que no estaban en el código inicial.
# en casos futuros, si 

# quita las columnas no utilizadas.
del df['Total Tests']
del df['Tests/1M pop']
del df['Region']

# y quita las líneas no utilizadas que corresponden a agrupaciones y sumas que se pueden hacer por otros medios.
# si las dejamos enviará valores duplicados al hacer sumas.

i = 0
while i < 8:
  df.drop(df.index[0],inplace=True)
  i += 1
    
# reinicia el índice del dataframe     
df.reset_index(drop=True, inplace=True)
    
# parámetros de conexión, se pueden poner en un fichero de configuración se deben de sustituir los parámetros entre <>
# por los que correspondan
engine = create_engine('postgresql+psycopg2://<usuario>:<password>@<host>:<puerto>/<base_de_datos>')

# en este caso la tabla se reescribe cada vez que el script sea ejecutado, para evitar duplicidad
df.to_sql('<tabla>', engine, if_exists='replace', index=False)

conn = engine.raw_connection()
cur = conn.cursor()
conn.commit()    
