import streamlit as st  
import pandas as pd
import plotly.express as px
from datetime import timedelta

def app_resume():
    @st.cache_data
    def load_data_cad():
        # Carregamento do dataframe de cadastro
        data_cad = pd.read_excel(r"content/cadastro.xlsx")
        date_columns = ['DTCONCLUSAO', 'DTAINC', 'DTAALT', 'DTINIDESLOCAMENTO', 'COMPETENCIA', 'DTAHORARECLAMACAO', 'DTCHEGADA']
        data_cad[date_columns] = data_cad[date_columns].apply(pd.to_datetime, errors='coerce')
        data_cad['PRAZO'] = data_cad['DTINIDESLOCAMENTO'] + timedelta(days=7)
        data_cad = data_cad.query("IDORIGEM == 2 & IDTIPOMANUTENCAO == 3")
        return data_cad

    @st.cache_data
    def load_data():
        # Substitua este bloco com a carga dos seus dados
        df = pd.read_excel(r"content/base_sip_Concluido.xlsx")
        str_columns = ['NUMOS', 'NUMOCORRENCIA', 'ROTA', 'UC', 'IDSIGFI', 'OBRA']
        df[str_columns] = df[str_columns].astype('str')
        return df

    def load_oem():
        df = load_data()
        # Buscar ultima data de preventivas e corretivas validadas
        lastdt = df['DATACONCLUSAO'].max()
        order_executed = df[df['DATACONCLUSAO'] == lastdt]
        # Separar das preventivas das corretivas já validadas.
        df_prev = order_executed.query("IDORIGEM == 2 & IDTIPOMANUTENCAO == 4 & STATUSSRV == 2")
        df_corr = order_executed.query("IDORIGEM == 2 & IDTIPOMANUTENCAO == 3 & STATUSSRV == 2")
        
        # Quantas OS's preventivas e corretivas foram executadas no dia (cards)
        count_prev = df_prev['NUMOS'].count()
        count_curr = df_corr['NUMOS'].count()
        
        # Criar os componentes do dashboard
        st.title('Dashboard de Manutenção')

        # Cards
        st.subheader('Análise')
        col1, col2 = st.columns(2)
        col1.metric("Preventivas Ontem", count_prev)
        col2.metric("Corretivas Ontem", count_curr)
        
        cad = load_data_cad()  # Supondo que a função load_data_cad() carrega os dados em um DataFrame

        # Contagem dos registros dentro do prazo
        count_within_deadline = cad[cad['DTINIDESLOCAMENTO'] <= cad['PRAZO']]['NUMOS'].count()

        # Contagem dos registros fora do prazo
        count_outside_deadline = cad[cad['DTINIDESLOCAMENTO'] > cad['PRAZO']]['NUMOS'].count()

        st.markdown(f"**{count_within_deadline}** ordens de serviço estão dentro do prazo.")
        st.markdown(f"**{count_outside_deadline}** ordens de serviço estão fora do prazo.")

        # Tabela de OS fora do prazo
        st.subheader('Ordens de Serviço fora do prazo')
        out_of_date_df = cad[cad['DTINIDESLOCAMENTO'] > cad['PRAZO']]
        st.write(out_of_date_df)

        # Gráficos
        st.subheader('Execução de ordens de serviço por dia')
        executions = df.groupby('DATACONCLUSAO').size().reset_index(name='Quantidade')
        fig = px.bar(executions, x='DATACONCLUSAO', y='Quantidade', labels={'Quantidade': 'Ordens de Serviço Executadas', 'DATACONCLUSAO': 'Data'})
        st.plotly_chart(fig)

    # Executar o aplicativo Streamlit
    st.write("Acompanhamento de produção")
    load_oem()  # Chama o dashboard automaticamente ao iniciar

# Chama a função principal
if __name__ == "__main__":
    app_resume()