import pandas as pd
import plotly.express as px
import streamlit as st

def ler_planilha():
    """Lê uma planilha do Excel."""
    excluir_status = ['TREINAMENTO', 'CADASTRO', 'TREINAMENTO']
    excluir_usuario = ['LUIZ.CARLOS']
    excluir_rota = [55, 70]
    df_bd = pd.read_excel(r"E:\OEM\content\base_sip_Concluido.xlsx")
    df = df_bd[~df_bd['STATUS'].isin(excluir_status)]
    df = df[~df['EXECUTOR'].isin(excluir_usuario)]
    df = df[~df['ROTA'].isin(excluir_rota)]
    return df

def aplicar_filtros(df, rota_value, status_value, tipo_value, executor_value, data_inicial, data_final, etapa_value):
    """Aplica filtros a uma planilha."""
    df_filtered = df[
        df["ROTA"].isin(rota_value) &
        df["STATUS"].isin(status_value) &
        df["TIPO"].isin(tipo_value) &
        df["EXECUTOR"].isin(executor_value) &
        df["ORIGEM"].isin(etapa_value) &
        (df["DTCONCLUSAO"] >= data_inicial) &
        (df["DTCONCLUSAO"] <= data_final)
    ]
    return df_filtered

def gerar_grafico(df_filtered):
    """Gera um gráfico com base nos dados filtrados."""
    grafico = pd.pivot_table(df_filtered, values='NUMOS', index=['ROTA'], columns=['STATUS'], aggfunc='count')
    fig = px.bar(grafico, barmode='stack')
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=list(grafico.index), ticktext=list(grafico.index)))
    fig.update_layout(xaxis_title='ROTA', yaxis_title='CONTAGEM', hovermode='closest')
    fig.update_layout(height=800, width=1280)  # Ajuste os valores conforme necessário
    st.plotly_chart(fig)

def mostrar_dataframe(df_filtered):
    """Mostra o DataFrame em formato de tabela."""
    st.dataframe(df_filtered[['NUMOS','NUMOCORRENCIA','UC','IDSIGFI','TIPOCAUSA','NOMECLIENTE','ROTA','STATUS','EXECUTOR','DTCONCLUSAO','LATLONCON']])

if __name__ == "__main__":
    df = ler_planilha()
    df["DTCONCLUSAO"] = pd.to_datetime(df["DTCONCLUSAO"]).dt.date

    # Criar filtros
    rota_options = list(df['ROTA'].unique())
    rota_filter = st.multiselect("Rotas:", rota_options)

    status_options = list(df['STATUS'].unique())
    status_filter = st.multiselect("Status:", status_options)

    tipo_options = list(df['TIPO'].unique())
    tipo_filter = st.multiselect("Tipo:", tipo_options)

    executor_options = list(df['EXECUTOR'].unique())
    executor_filter = st.multiselect("Usuário:", executor_options)

    etapa_options = list(df['ORIGEM'].unique())
    etapa_filter = st.multiselect("Etapa:", etapa_options)

    data_inicial_filter = st.date_input("Data Inicial:", value=df["DTCONCLUSAO"].min())
    data_final_filter = st.date_input("Data Final:", value=df["DTCONCLUSAO"].max())

    # Criar botões
    aplicar_filter_button = st.button("Aplicar Filtro")
    apresentar_tabela_button = st.button("Apresentar Tabela")
    gerar_grafico_button = st.button("Gerar Gráfico")

    if aplicar_filter_button:
        df_filtered = aplicar_filtros(df, rota_filter, status_filter, tipo_filter, executor_filter, data_inicial_filter, data_final_filter, etapa_filter)

    if apresentar_tabela_button:
        mostrar_dataframe(df_filtered)

    if gerar_grafico_button:
        gerar_grafico(df_filtered)
