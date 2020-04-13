# Práctica 1: Web scraping

## Descripción

Esta práctica se ha realizado bajo el contexto de la asignatura _Tipología y ciclo de vida de los datos_, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En ella, se aplican técnicas de _web scraping_ mediante el lenguaje de programación Python para extraer así datos de la web _www.worldometers.info_, en particular en lo referente a los datos de la pandemia relacionada con el Covid-19, la cual viene con detalle por país y generar contiene el conjunto de datos en formato tabla.

## Miembros del equipo

La actividad ha sido realizada de manera individual por **Alejandro De La Concha**.

## Ficheros del código fuente
(Se encuentran en el folder _notebook_)

* **coronavirus_ws_to_csv.ipynt**: contiene el Notebook en Python dedicado a hacer el _Web Scraping_ que a su vez genera el conjunto de datos a partir de la información online [www.worldometers.info](https://www.worldometers.info/coronavirus/). El script busca la tabla de detalle de casos por país, la cual es actualizada cada minuto por el sitio web mencionado. El script genera un dataframe que después es exportado a un fichero CSV (_Comma Separated Value_).
* **coronavirus_ws_to_db.ipynt**: Es casi igual que el fichero anterior con la variante de escribir en una base de datos, en mi caso seleccioné este método para poder visualizar los resultados. Al escribir en una base de datos se puede actualizar en sincronía con la fuente. Haciendo un script que se ejecute cada minuto y sobreescriba los valores en una tabla. También al quedar en una base de datos se pueden hacer cosas interesantes con código SQL como JOINS con tablas de región y características de los países que nos puedan aportar más profundidad de análisis, en mi caso he utilizado una tabla de países por continente/región para hacer análisis más agergado y también por localización para poder ubicar los datos de la tabla en una visualización tipo mapa.

(Se encuentre en el folder _script_)
* **coronavirus_ws.py**: Es el código utilizado para hacer de forma recurrente el _web scraping_ de la fuente, es similar al notebook _coronavirus_ws_to_db.ipynt_, pero sin las validaciones intermedias. 

## Ficheros de datos
(Se encuentran en el folder _csv_)

* **covid19_cases_by_country.csv**: contiene un ejemplo de extracción de datos desde el script _coronavirus_ws_to_csv.ipynt_, en este fichero se ha dejado la columna de index del dataframe la cual se podía eliminar en el script o bien en un paso posterior de análisis, decidí dejarla.
* **countries.csv**: contiene los datos de relación de país con continente/región y código de dos letras para ser utilizado en la base de datos y herramientas de visualización y análisis, al hacer JOIN con el _dataset_ de casos por país se pueden obtener análsisi adicionales más agregados como casos por continente o región o visualizaciones asociadas a mapas. 

## Recursos

1. Lawson, R. (2015). _Web Scraping with Python_. Packt Publishing Ltd. Chapter 2. Scraping the Data.
2. Mitchel, R. (2015). _Web Scraping with Python: Collecting Data from the Modern Web_. O'Reilly Media, Inc. Chapter 1. Your First Web Scraper.
3. Subirats, L., Calvo, M. (2018). Web Scraping. Editorial UOC.
4. Masip, D. El lenguaje Python. Editorial UOC.
5. Simon Munzert, Christian Rubba, Peter Meißner, Dominic Nyhuis. (2015).
6. Automated Data Collection with R: A Practical Guide to Web Scraping and Text Mining. John Wiley & Sons.
7. Tutorial de Github [https://guides.github.com/activities/hello-world](https://guides.github.com/activities/hello-world).
