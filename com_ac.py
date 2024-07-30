import pandas as pd
import streamlit as st  
import plotly.express as px
import sqlite3

#Função para conectar ao Banco de Dados SQLite
def conectar_bd():
    conn = sqlite3.connect('dados_comissionamento.db')
    return conn
# Passo 3: Criar a Tabela no Banco de Dados
def criar_tabela():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comissionamento (
        IDSERVICOSCONJ INTEGER PRIMARY KEY,
        ROTA INTEGER,
        CONCLUSAO DATE,
        STATUS TEXT,
        USUARIO TEXT,
        NOMEDOCLIENTE TEXT,
        OBSERVACAOINT TEXT,
        LATLONCONF TEXT,
        ENDERECO TEXT,
        MUNICIPIO TEXT,
        ETAPA TEXT,
        USUARIOALT TEXT,
        LATITUDE REAL,
        LONGITUDE REAL
    )
    """)
    conn.commit()
    conn.close()
 #Modificar a Função de Armazenamento de Dados   
def armazenar_dados(df):
    conn = conectar_bd()
    cursor = conn.cursor()
    for _, row in df.iterrows():
        try:
            cursor.execute("""
            INSERT INTO comissionamento (IDSERVICOSCONJ, ROTA, CONCLUSAO, STATUS, USUARIO, NOMEDOCLIENTE, OBSERVACAOINT, LATLONCONF, ENDERECO, MUNICIPIO, ETAPA, USUARIOALT, LATITUDE, LONGITUDE)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (row['IDSERVICOSCONJ'], row['ROTA'], row['CONCLUSAO'], row['STATUS'], row['USUARIO'], row['NOMEDOCLIENTE'], row['OBSERVACAOINT'], row['LATLONCONF'], row['ENDERECO'], row['MUNICIPIO'], row['ETAPA'], row['USUARIOALT'], row['LATITUDE'], row['LONGITUDE']))
            conn.commit()
        except sqlite3.IntegrityError as e:
            st.warning(f"Dados duplicados não adicionados: {row['IDSERVICOSCONJ']}. Erro: {e}")
    conn.close()
    st.success("Dados armazenados com sucesso no banco de dados.")

def filter_com():
    st.title("COMISSIONAMENTOS LOTE 01 & 02")    

    @st.cache_data
    def ler_planilha():
        """Lê uma planilha do Excel."""
        excluir_status = ['TREINAMENTO', 'CADASTRO', 'TREINAMENTO']
        excluir_usuario = ['LUIZ.CARLOS']
        excluir_rota = [599,600]
        df_bd = pd.read_excel(r"content\base_sip_instalacoes_Geral_ac.xlsx")
        df = df_bd[~df_bd['STATUS'].isin(excluir_status)]
        df = df[~df['USUARIO'].isin(excluir_usuario)]
        df = df[~df['ROTA'].isin(excluir_rota)]
        return df

    @st.cache_data
    def aplicar_filtros(df, rota_value, status_value, tipo_value, usuario_value, data_inicial, data_final, etapa_value):
        """Aplica filtros a uma planilha."""
        df_filtered_ac = df[
            df["ROTA"].isin(rota_value) &
            df["STATUS"].isin(status_value) &
            df["TIPO"].isin(tipo_value) &
            df["USUARIO"].isin(usuario_value) &
            df["ETAPA"].isin(etapa_value) &
            (df["CONCLUSAO"] >= data_inicial) &
            (df["CONCLUSAO"] <= data_final)
        ]
        return df_filtered_ac

    def gerar_grafico(df_filtered_ac):
        """Gera um gráfico com base nos dados filtrados."""
        grafico = pd.pivot_table(df_filtered_ac, values='IDSERVICOSCONJ', index=['ROTA'], columns=['STATUS'], aggfunc='count')
        fig = px.bar(grafico, barmode='stack')
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=list(grafico.index), ticktext=list(grafico.index)))
        fig.update_layout(xaxis_title='ROTA', yaxis_title='CONTAGEM', hovermode='closest')
        fig.update_layout(height=800, width=1280)
        st.plotly_chart(fig)

    def mostrar_dataframe(df_filtered_ac):
        """Mostra o DataFrame em formato de tabela."""
        # Adiciona uma coluna de checkboxes ao DataFrame
        df_filtered_ac['Selecionar'] = [False] * len(df_filtered_ac)

        # Exibe o DataFrame com a coluna de checkboxes
        st.dataframe(df_filtered_ac[['Selecionar','IDSERVICOSCONJ','ROTA','CONCLUSAO','STATUS','USUARIO',
                                  'NOMEDOCLIENTE','OBSERVACAOINT','LATLONCONF','ENDERECO','MUNICIPIO','ETAPA','USUARIOALT']])
        
        # Acessa o valor máximo da coluna "IDSERVICOSCONJ"
        favorite_command = df_filtered_ac["IDSERVICOSCONJ"].max()
        st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
        
        
    df = ler_planilha()
    df["CONCLUSAO"] = pd.to_datetime(df["CONCLUSAO"]).dt.date

    col01_dt, col02_dt = st.columns(2)
    data_inicial_filter = col01_dt.date_input("Data Inicial:", value=df["CONCLUSAO"].min())
    data_final_filter = col02_dt.date_input("Data Final:", value=df["CONCLUSAO"].max())

    col01_tipo, col02_status, col3_etapa = st.columns(3)

    etapa_options = sorted(list(df['ETAPA'].unique()))
    etapa_filter = col3_etapa.multiselect("Etapa:", etapa_options)

    tipo_options = sorted(list(df['TIPO'].unique()))
    tipo_filter = col01_tipo.multiselect("Tipo:", tipo_options)

    status_options = sorted(list(df['STATUS'].unique()))
    status_filter = col02_status.multiselect("Status:", status_options)

    rota_options = sorted(list(df.loc[df['ROTA'].notna(),'ROTA'].unique()))

    rota_check_all = st.checkbox("Selecionar projeto Geral")
    rota_check_all_hoppecke = st.checkbox("Selecionar projeto Hoppecke")
    rota_check_all_intelbras = st.checkbox("Selecionar projeto Intelbras")

    if rota_check_all_hoppecke:
        hoppecke_options = [rota for rota in rota_options if 50 <= int(rota) <= 59]
        rota_filter = st.multiselect("Rotas Hoppecke:", hoppecke_options, default=hoppecke_options)
    elif rota_check_all_intelbras:
        intelbras_options = [rota for rota in rota_options if 1 <= int(rota) <= 49]
        rota_filter = st.multiselect("Rotas Intelbras:", intelbras_options, default=intelbras_options)
    elif rota_check_all:
        rota_filter = st.multiselect("Rotas:", rota_options, default=rota_options)
    else:
        rota_filter = st.multiselect("Rotas:", rota_options)

    usuario_options = sorted(list(df.loc[df['USUARIO'].notna(),'USUARIO'].unique()))
    usuario_check_all = st.checkbox("Selecionar todos Usuários")

    if usuario_check_all:
        usuario_filter = st.multiselect("Usuário:", usuario_options, default=usuario_options)
    else:
        usuario_filter = st.multiselect("Usuário:", usuario_options)

    df_filtered_ac = aplicar_filtros(df, rota_filter, status_filter, tipo_filter, usuario_filter, data_inicial_filter, data_final_filter, etapa_filter)

    # Crie duas colunas lado a lado
    col1, col2 = st.columns(2)
    # Botão "Apresentar Tabela"
    if col1.button("Apresentar Tabela"):
        if df_filtered_ac.empty:
            st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
        else:
            mostrar_dataframe(df_filtered_ac)
    # Botão "Gerar Gráfico"
    if col2.button("Gerar Gráfico"):
        if df_filtered_ac.empty:
            st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
        else:
            gerar_grafico(df_filtered_ac)
    #Botão de armazenamento no sqlite
    if st.button("Armazenar Dados"):
        if df_filtered_ac.empty:
            st.warning("Não há dados para armazenar.")
        else:
            armazenar_dados(df_filtered_ac)
filter_com()