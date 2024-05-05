import streamlit as st
import webbrowser
import pandas as pd
import googlemaps
import sqlite3


# Chave de API do Google Maps (substitua pela sua chave)
api_key = 'AIzaSyDCL6ERb5rPN8nTVloJ5UuG0ALAlFoAUeU'

# Criar o cliente do Google Maps
client = googlemaps.Client(key=api_key)

# Função para abrir o Google Maps em uma nova janela do navegador
def open_google_maps(lat, lon):
    url = f"https://www.google.com/maps/@{lat},{lon},15z"
    webbrowser.open_new_tab(url)

# Carregar dados do banco de dados SQLite
def load_data():
    conn = sqlite3.connect('dados_comissionamento.db')
    query = "SELECT * FROM comissionamento"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title('Gerador de Mapas')

# Carregar DataFrame
df = load_data()

if not df.empty:
    options = df['ROTA'].dropna().unique()
    selected_options = st.multiselect('Escolha uma Rota:', options)
    
    if st.button('Gerar Mapa'):
        customer_data = df[df['ROTA'].isin(selected_options)]
        if not customer_data.empty:
            map_df = customer_data[['LATITUDE', 'LONGITUDE']]
            map_df.columns = ['lat', 'lon']
            
            if not map_df['lat'].isnull().any() and not map_df['lon'].isnull().any():
                st.map(map_df, zoom=12)
                
                # Aqui, consideramos abrir apenas a primeira localização para evitar múltiplas abas
                first_location = customer_data.iloc[0]
                open_google_maps(first_location['LATITUDE'], first_location['LONGITUDE'])
            else:
                st.error('Algumas coordenadas são inválidas para as rotas selecionadas.')
        else:
            st.error('Dados não encontrados para as rotas selecionadas.')
else:
    st.error('Nenhum dado encontrado no banco de dados.')