import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache_data(ttl=600)  # Use st.cache_data com ttl (time-to-live) em segundos
def ler_planilha():
    excluir_status = ['TREINAMENTO', 'CADASTRO', 'TREINAMENTO']
    excluir_usuario = ['LUIZ.CARLOS']
    excluir_rota = [55, 70]
    df_bd = pd.read_excel(r'C:\Users\helym\projeto_python\dash\dash_oem\content\base_sip_Concluido.xlsx')
    df = df_bd[~df_bd['STATUS'].isin(excluir_status)]
    df = df[~df['EXECUTOR'].isin(excluir_usuario)]
    df = df[~df['ROTA'].isin(excluir_rota)]
    return df

@st.cache_data(ttl=600)  # Use st.cache_data com ttl (time-to-live) em segundos
def aplicar_filtros(df, rota_value, status_value, tipo_value, executor_value, data_inicial, data_final, etapa_value):
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
    grafico = pd.pivot_table(df_filtered, values='NUMOS', index=['ROTA'], columns=['STATUS'], aggfunc='count')
    fig = px.bar(grafico, barmode='stack')
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=list(grafico.index), ticktext=list(grafico.index)))
    fig.update_layout(xaxis_title='ROTA', yaxis_title='CONTAGEM', hovermode='closest')
    fig.update_layout(height=800, width=1280)
    st.plotly_chart(fig)

def mostrar_dataframe(df_filtered):
    st.dataframe(df_filtered[['NUMOS', 'NUMOCORRENCIA', 'UC', 'IDSIGFI', 'TIPOCAUSA', 'NOMECLIENTE', 'ROTA', 'STATUS', 'EXECUTOR', 'DTCONCLUSAO', 'LATLONCON']])

if __name__ == "__main__":
    df = ler_planilha()
    df["DTCONCLUSAO"] = pd.to_datetime(df["DTCONCLUSAO"]).dt.date

    rota_options = sorted(list(df['ROTA'].unique()))
    rota_filter = st.multiselect("Rotas:", rota_options)

    status_options = sorted(list(df['STATUS'].unique()))
    status_filter = st.multiselect("Status:", status_options)

    tipo_options = sorted(list(df['TIPO'].unique()))
    tipo_filter = st.multiselect("Tipo:", tipo_options)

    executor_options = sorted(list(df['EXECUTOR'].unique()))
    executor_filter = st.multiselect("Usuário:", executor_options)

    etapa_options = sorted(list(df['ORIGEM'].unique()))
    etapa_filter = st.multiselect("Etapa:", etapa_options)

    data_inicial_filter = st.date_input("Data Inicial:", value=df["DTCONCLUSAO"].min())
    data_final_filter = st.date_input("Data Final:", value=df["DTCONCLUSAO"].max())

    df_filtered = aplicar_filtros(df, rota_filter, status_filter, tipo_filter, executor_filter, data_inicial_filter, data_final_filter, etapa_filter)

    if st.button("Apresentar Tabela"):
        if df_filtered is None or df_filtered.empty:
            st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
        else:
            mostrar_dataframe(df_filtered)

    if st.button("Gerar Gráfico"):
        if df_filtered is None or df_filtered.empty:
            st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
        else:
            gerar_grafico(df_filtered)
