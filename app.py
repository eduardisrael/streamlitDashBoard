import streamlit as st
import  pandas as pd
import numpy as np

st.title("Analisis de Sentimientos de los tweets sobre las Aerolineas")
st.sidebar.title("Analisis de Sentimientos de los tweets sobre las Aerolineas")

st.markdown("Esta App es un Streamlit Dashboard para analisis los sentimientos de los tweets 🐦")
st.sidebar.markdown("Esta App es un Streamlit Dashboard para analisis los sentimientos de los tweets 🐦")

@st.cache(persist=True) #Persiste en cache para optimizar, solo si cambia ejecuta
DATA_URL = ("/home/rhyme/Desktop/Projects/Tweets.csv")
def cargar_datos():
    data = pd.read_csv(DATA_URL)
    data.['teet_created'] = pd.to_datetime(data['tweet_created']) #standard date Pandas
    return data

data = cargar_datos()
