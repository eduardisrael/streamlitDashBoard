import streamlit as st
import  pandas as pd
import numpy as np

st.title("Analisis de Sentimientos de los tweets sobre las Aerolineas")
st.sidebar.title("Analisis de Sentimientos de los tweets sobre las Aerolineas")

st.markdown("Esta App es un Streamlit Dashboard para analisis los sentimientos de los tweets 🐦")
st.sidebar.markdown("Esta App es un Streamlit Dashboard para analisis los sentimientos de los tweets 🐦")

DATA_URL = ("/home/rhyme/Desktop/Project/Tweets.csv")

@st.cache(persist=True) #Persiste en cache para optimizar, solo si cambia ejecuta
def cargar_datos():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created']) #standard date Pandas
    return data

data = cargar_datos()

st.sidebar.subheader("Mostrar tweets aleatorios")
random_tweet = st.sidebar.radio('Sentimento',('positive','neutral','negative')) #depende del csv

#consultar nuestro marco de datos, especificamente Airline, con el sentimiento
 #texto de la columna de datos, funcion sample (muestras azar)de pandas, solo uno, nuestra texto columna 0,0
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])
