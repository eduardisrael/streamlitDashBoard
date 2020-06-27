import streamlit as st
import  pandas as pd
import numpy as np
import plotly.express as px

st.title("Analisis de Sentimientos de los Tweets sobre las Aerolineas")
st.sidebar.title("Analisis de Sentimientos de los tweets: Aerolineas")

st.markdown("Esta App es un Streamlit Dashboard para analisis los sentimientos de los tweets 🐦")
st.sidebar.markdown("Esta App es un Streamlit Dashboard para analisis los sentimientos de los tweets 🐦")

DATA_URL = ("./Tweets.csv")

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

st.sidebar.markdown("### Numero de tweets por sentimiento")
#Widget, agregamos parametro key=1, nos permite es usar el cuadro de seleccion de la barra
seleccion = st.sidebar.selectbox('Tipo de Visualizacion',['Histograma','Pie Chart'], key='1')

#nuevo marco de datos, y funcion para contar los datos - st.write(contadorSentimiento)
contadorSentimiento = data['airline_sentiment'].value_counts()
#creamos tramas, express espera un marco de datos ordenado como entrada
#los sentimientos reales fueron almacenados en el indice del panda, columna tweets en lugar de indexar sus valores
contadorSentimiento = pd.DataFrame({'Sentimiento':contadorSentimiento.index, 'Tweets':contadorSentimiento.values})


if not st.sidebar.checkbox("Hide", True):
    st.markdown("### Numero de tweets por sentimiento")
    if seleccion == "Histograma":
        fig = px.bar(contadorSentimiento, x='Sentimiento', y='Tweets', color='Tweets', height=500) #eje x,y index, values
        st.plotly_chart(fig)
    else:
        #necesitamos pasar valores y nombres -- PieChart
        fig = px.pie(contadorSentimiento, values='Tweets', names='Sentimiento')
        st.plotly_chart(fig)
