#Israel Pasaca

import streamlit as st
import  pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import wordcloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Análisis de Sentimientos de los Tweets: Aerolíneas")
st.sidebar.title("Análisis de Sentimientos de los tweets: Aerolíneas")

st.markdown("Esta App es un Streamlit Dashboard para analisis los sentimientos de los tweets 🐦")
st.sidebar.markdown("Esta App es un Streamlit Dashboard para análisis los sentimientos de los tweets 🐦")

DATA_URL = ("./Tweets.csv")

@st.cache(persist=True) #Decorator, persiste en cache para optimizar, solo si cambia se ejecuta
def cargar_datos():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created']) #standard date Pandas
    return data

data = cargar_datos()

st.sidebar.subheader("Mostrar tweets aleatorios")
random_tweet = st.sidebar.radio('Sentimento',('positive','neutral','negative')) #csv

#consultar nuestro marco de datos, especificamente Airline, con el sentimiento
#texto de la columna de datos, funcion sample (muestras aleatoria ) de pandas, solo uno, texto columna 0,0
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Numero de tweets por sentimiento")

#Widget, agregamos parametro key=1, nos permite es usar el cuadro de seleccion de la barra
seleccion = st.sidebar.selectbox('Tipo de Visualizacion',['Histograma','Pie Chart'], key='1')

#nuevo marco de datos, y funcion para contar los datos - st.write(contadorSentimiento)
contadorSentimiento = data['airline_sentiment'].value_counts()

#creamos tramas, express espera un marco de datos ordenado como entrada
#los sentimientos reales fueron almacenados en el indice del panda, columna tweets en lugar de indexar sus valores
contadorSentimiento = pd.DataFrame({'Sentimiento':contadorSentimiento.index, 'Tweets':contadorSentimiento.values})


if not st.sidebar.checkbox("Ocultar", True):
    st.markdown("### Numero de tweets por sentimiento")
    if seleccion == "Histograma":
        fig = px.bar(contadorSentimiento, x='Sentimiento', y='Tweets', color='Tweets', height=500) #eje x,y index, values
        st.plotly_chart(fig)
    else:
        #necesitamos pasar valores y nombres -- PieChart
        fig = px.pie(contadorSentimiento, values='Tweets', names='Sentimiento')
        st.plotly_chart(fig)


#solo si existe Latitud, longitud or long,short st.map(data)
#hour= st.sidebar.number_input("Hora del día", min_value=1, max_value=24)
#libreria de pandas para filtrar datos por la hora del dia 
st.sidebar.subheader("¿Dónde y cuándo estan enviando Tweets los usuarios?")
hora = st.sidebar.slider("Hora del día", 0, 23)
datosModificados = data[data["tweet_created"].dt.hour == hora]

if not st.sidebar.checkbox("Ocultar", True, key='1'):
    st.markdown("### Ubicacion de los tweets por hora del día")

    #numero de tweets en total, hora, incremento/finaliza, arthm values limited
    st.markdown("%i tweets entre %i:00 - %i:00" % (len(datosModificados),hora,(hora+1)%24)) 
    st.map(datosModificados)

    #si verificacion muestra datos sin procesar marcados, podemos mostrar los datos modificados
    if st.sidebar.checkbox("Mostrar fila de datos", False):
        #raw data , no mostrara por defecto
        #si marcan, a dashborad
        st.write(datosModificados)


st.sidebar.subheader("Desglose de Tweets por sentimiento")
opcion = st.sidebar.multiselect("Selecciona Aerolinea",('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key=0)

if (len(opcion)) > 0:
    #Aseguramos seleccionar aerolineas correctas, desde el marco de datos retornado un subconjunto
    data_opcion = data[data.airline.isin(opcion)]
    
    #histfunc eje y, tramas - cada opcion 3 bar plots
    #Label: diccionario de etiquetas
    fig_opcion = px.histogram(data_opcion, x='airline', y='airline_sentiment', histfunc='count',
                 color='airline_sentiment', facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'}, 
                 height=600, width=800)
    st.plotly_chart(fig_opcion)


st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Mostrar 'WordCloud', ¿Que sentimento?',('positve','neutral','negative'))










