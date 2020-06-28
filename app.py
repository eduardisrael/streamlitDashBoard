#Israel Pasaca

import streamlit as st
import  pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Análisis de Sentimientos de los Tweets: Aerolíneas")
st.sidebar.title("Análisis de Sentimientos de los tweets: Aerolíneas")

st.markdown("Esta App es un Streamlit Dashboard para analisis los sentimientos de los tweets 🐦")
st.sidebar.markdown("Esta App es un Streamlit Dashboard para análisis los sentimientos de los tweets 🐦")

DATA_URL = ("./Tweets.csv")

@st.cache(persist=True) 
def cargar_datos():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created']) #standard date Pandas
    return data

data = cargar_datos()

st.sidebar.subheader("Mostrar tweets aleatorios")
random_tweet = st.sidebar.radio('Sentimento',('positive','neutral','negative')) #csv
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])
st.sidebar.markdown("### Numero de tweets por sentimiento")
seleccion = st.sidebar.selectbox('Tipo de Visualizacion',['Histograma','Pie Chart'], key='1')

contadorSentimiento = data['airline_sentiment'].value_counts()
contadorSentimiento = pd.DataFrame({'Sentimiento':contadorSentimiento.index, 'Tweets':contadorSentimiento.values})

if not st.sidebar.checkbox("Ocultar", True):
    st.markdown("### Numero de tweets por sentimiento")
    if seleccion == "Histograma":
        fig = px.bar(contadorSentimiento, x='Sentimiento', y='Tweets', color='Tweets', height=500) #eje x,y index, values
        st.plotly_chart(fig)
    else:
        fig = px.pie(contadorSentimiento, values='Tweets', names='Sentimiento')
        st.plotly_chart(fig)


st.sidebar.subheader("¿Dónde y cuándo estan enviando Tweets los usuarios?")
hora = st.sidebar.slider("Hora del día", 0, 23)
datosModificados = data[data["tweet_created"].dt.hour == hora]

if not st.sidebar.checkbox("Ocultar", True, key='1'):
    st.markdown("### Ubicacion de los tweets por hora del día")
    st.markdown("%i tweets entre %i:00 - %i:00" % (len(datosModificados),hora,(hora+1)%24)) 
    st.map(datosModificados)

    if st.sidebar.checkbox("Mostrar fila de datos", False):
        st.write(datosModificados)


st.sidebar.subheader("Desglose de Tweets por sentimiento")
opcion = st.sidebar.multiselect("Selecciona Aerolinea",('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key=0)

if (len(opcion)) > 0:
    data_opcion = data[data.airline.isin(opcion)]
    fig_opcion = px.histogram(data_opcion, x='airline', y='airline_sentiment', histfunc='count',
                 color='airline_sentiment', facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'}, 
                 height=600, width=800)
    st.plotly_chart(fig_opcion)


st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Mostrar WordCloud, ¿Que sentimento?',('positive','neutral','negative'))

if not st.sidebar.checkbox("Ocultar", True, key=3):
    st.header('Word Cloud: %s' % (word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])

    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])    
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words) 

    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()