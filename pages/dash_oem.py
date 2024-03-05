import streamlit as st  
import pandas as pd
import plotly.express as px
from datetime import timedelta

@st.cache
def load_data():
    # Substitua este bloco com a carga dos seus dados
    data = pd.read_excel(r'C:\Users\helym\.streamlit\dashboard\content\base_sip_Concluido.xlsx')
    df = pd.DataFrame(data)
    df = df.loc[df['ORIGEM'] == 'ENERGISA']
    str_columns = ['NUMOS', 'NUMOCORRENCIA', 'ROTA', 'UC', 'IDSIGFI', 'OBRA']
    df[str_columns] = df[str_columns].astype('str')
    date_columns = ['DTCONCLUSAO', 'DTAINC', 'DTAALT', 'DTINIDESLOCAMENTO', 'COMPETENCIA', 'DTAHORARECLAMACAO', 'DTCHEGADA']
    df[date_columns] = df[date_columns].apply(pd.to_datetime)
    #df['PRAZO'] = df['DTINIDESLOCAMENTO'] + timedelta(days=7)
    return df

def app_oem():
    df = load_data()

    # Separar das preventivas das corretivas.
    df_prev = df.loc[df['TIPO'] == 'PREVENTIVAS']
    df_corr = df.loc[df['TIPO'] == 'CORRETIVAS']
    
    #Preciso saber quantas os's preventivas foram executada no dia[card]
    date_ultimate = df_prev['DATACONCLUSAO'].max()
    current_day_prev = df_prev[df_prev['DATACONCLUSAO'] == date_ultimate]
    df_prev_day_prev = current_day_prev['NUMOS'].count()
    #Preciso saber quantas os's corretivas foram executada no dia[card]
    date_ultimate = df_corr['DATACONCLUSAO'].max()
    current_day_corr = df_corr[df_corr['DATACONCLUSAO'] == date_ultimate]
    df_prev_day_corr = current_day_corr['NUMOS'].count()
    
    # Criar os componentes do dashboard
    st.title('Dashboard de Manutenção')

    # Cards
    st.subheader('Análise')
    col1, col2 = st.columns(2)
    col1.metric("Preventivas Hoje", df_prev_day_prev)
    col2.metric("Corretivas Hoje", df_prev_day_corr)
  
    st.markdown(f"**{df[df['STATUS']=='CADASTRO'].shape[0]}** ordens de serviço estão dentro do prazo.")
    st.markdown(f"**{df[df['STATUS']!='CADASTRO'].shape[0]}** ordens de serviço estão fora do prazo.")

    # Tabela animada
    st.subheader('Ordens de Serviço fora do prazo')
    out_of_date_df = df[df['DTINIDESLOCAMENTO'] > df['PRAZO']]
    st.write(out_of_date_df)

    # Gráficos
    st.subheader('Execução de ordens de serviço por dia')
    executions = df.groupby('DATACONCLUSAO').size().reset_index(name='Quantidade')
    fig = px.bar(executions, x='DATACONCLUSAO', y='Quantidade', labels={'Quantidade': 'Ordens de Serviço Executadas', 'DATACONCLUSAO': 'Data'})
    st.plotly_chart(fig)

#Executar o aplicativo Streamlit
if __name__ == '__main__':
    st.write("Exemplo de dashboard interativo usando Streamlit.")
    dashboard_clicked = st.sidebar.button("Dashboard O&M", type="primary")
    if dashboard_clicked:
        app_oem()
