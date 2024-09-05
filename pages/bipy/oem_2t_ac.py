import streamlit as st  
import pandas as pd
import numpy as np
#import plotly.express as px

def base_oem_2t_ac():
    st.title("O&M 2ª Tranche Acre")
    
    @st.cache_data
    def reader_data():
       """Lê a planilha informada"""
       del_rota = [599,600]
       bd = pd.read_excel(r"C:\Users\OneEngInst\Projetos_python\dashboard\content\base_sip_Concluido.xlsx")
       bd = bd[bd.ROTA.isin(del_rota) == False]
       bd = bd.loc[(bd['IDORIGEM'].isin([2]))]
       bd = bd.loc[(bd['ROTA'].isin([14,15,16,17,21,22,23,24]))]
       bd = bd.loc[(bd['STATUSSRV'].isin([1,2,3,4,6]))]
       bd = bd.loc[(bd['IDTIPOMANUTENCAO'].isin([4]))]
       bd[['IDSIGFI', 'UC', 'ROTA', 'NUMOS']] = bd[['IDSIGFI', 'UC', 'ROTA', 'NUMOS']].astype(str)
       bd = bd[['IDSIGFI','UC','NOMECLIENTE','ROTA','NUMOS','STATUS','LATLONCON','MUNICIPIO', 'ENDERECO','DTCONCLUSAO','IDTIPOSOLICITACAO']] 
       return bd
    
    @st.cache_data
    def reader_data_ins():
         """Lê a planilha de instalações"""
         del_status = ['TREINAMENTO','TREINAMENTO','CANCELADO','CANCELADO         ','DUPLICADOS']
         del_rota = [599,600]
         bd_ins = pd.read_excel(r"C:\Users\OneEngInst\Projetos_python\dashboard\content\base_sip_instalacoes_Geral_ac.xlsx")
         bd_ins = bd_ins[~bd_ins.ROTA.isin(del_rota)]
         bd_ins = bd_ins[~bd_ins.STATUS.isin(del_status)]
         bd_ins = bd_ins.loc[(bd_ins['TIPO'] == 'INS')]
         bd_ins = bd_ins.loc[(bd_ins['IDEMPRESA'].isin([1]))]
         bd_ins = bd_ins.loc[(bd_ins['ROTA'].isin([14,15,16,17,21,22,23,24]))]
         bd_ins = bd_ins.loc[(bd_ins['ETAPA'].isin([3]))]
         bd_ins['IDSERVICOSCONJ'] = bd_ins['IDSERVICOSCONJ'].astype(str)
         bd_ins = bd_ins[['IDSERVICOSCONJ','CODIGOENERGISA','NOMEDOCLIENTE','ROTA','MUNICIPIO', 'ENDERECO','CONCLUSAO','LATITUDE',
                            'LONGITUDE']]
         return bd_ins
   
    # Lê os dados
    bd = reader_data()
    # Contagem sistema existentes
    bd_ins = reader_data_ins()
    count_oem = bd['NUMOS'].count()
    count_oem = np.int64(count_oem)
    count_bdins = bd_ins['IDSERVICOSCONJ'].count()
    count_bdins = np.int64(count_bdins)
    #Contagem por ciclos 1A
    cycle_1a = bd.loc[bd['IDTIPOSOLICITACAO'] == 11]
    count_cycle_1a = cycle_1a['IDSIGFI'].count()
    count_cycle_1a = np.int64(count_cycle_1a)
    count_cycle_1a = int(count_cycle_1a)
    delta_1a = count_cycle_1a - count_bdins
    delta_1a = np.int64(delta_1a)
    delta_1a = int(delta_1a)
    #Contagem por ciclos 2A
    cycle_2a = bd.loc[bd['IDTIPOSOLICITACAO'] == 39]
    count_cycle_2a = cycle_2a['IDSIGFI'].count()
    count_cycle_2a = np.int64(count_cycle_2a)
    count_cycle_2a = int(count_cycle_2a)
    delta_2a = count_cycle_2a - count_bdins
    delta_2a = np.int64(delta_2a)
    delta_2a = int(delta_2a)
    #Contagem por ciclos 3A
    cycle_3a = bd.loc[bd['IDTIPOSOLICITACAO'] == 40]
    count_cycle_3a = cycle_3a['IDSIGFI'].count()
    count_cycle_3a = np.int64(count_cycle_3a)
    count_cycle_3a = int(count_cycle_3a)
    delta_3a = count_cycle_3a - count_bdins
    delta_3a = np.int64(delta_3a)
    delta_3a = int(delta_3a)
    #Contagem por ciclos 4A
    cycle_4a = bd.loc[bd['IDTIPOSOLICITACAO'] == 41]
    count_cycle_4a = cycle_4a['IDSIGFI'].count()
    count_cycle_4a = np.int64(count_cycle_4a)
    count_cycle_4a = int(count_cycle_4a)
    delta_4a = count_cycle_4a - count_bdins
    delta_4a = np.int64(delta_4a)
    delta_4a = int(delta_4a)
    #Contagem por ciclos 5A
    cycle_5a = bd.loc[bd['IDTIPOSOLICITACAO'] == 42]
    count_cycle_5a = cycle_5a['IDSIGFI'].count()
    count_cycle_5a = np.int64(count_cycle_5a)
    count_cycle_5a = int(count_cycle_5a)
    delta_5a = count_cycle_5a - count_bdins
    delta_5a = np.int64(delta_5a)
    delta_5a = int(delta_5a)
    #Contagem por ciclos 6A
    cycle_6a = bd.loc[bd['IDTIPOSOLICITACAO'] == 43]
    count_cycle_6a = cycle_6a['IDSIGFI'].count()
    count_cycle_6a = np.int64(count_cycle_6a)
    count_cycle_6a = int(count_cycle_6a)
    delta_6a = count_cycle_6a - count_bdins
    delta_6a = np.int64(delta_6a)
    delta_6a = int(delta_6a)
    #Contagem por ciclos 7A
    cycle_7a = bd.loc[bd['IDTIPOSOLICITACAO'] == 44]
    count_cycle_7a = cycle_7a['IDSIGFI'].count()
    count_cycle_7a = np.int64(count_cycle_7a)
    count_cycle_7a = int(count_cycle_7a)
    delta_7a = count_cycle_7a - count_bdins
    delta_7a = np.int64(delta_7a)
    delta_7a = int(delta_7a)
    #Contagem por ciclos 8A
    cycle_8a = bd.loc[bd['IDTIPOSOLICITACAO'] == 45]
    count_cycle_8a = cycle_8a['IDSIGFI'].count()
    count_cycle_8a = np.int64(count_cycle_8a)
    count_cycle_8a = int(count_cycle_8a)
    delta_8a = count_cycle_8a - count_bdins
    delta_8a = np.int64(delta_8a)
    delta_8a = int(delta_8a)
    #Contagem por ciclos 9A
    cycle_9a = bd.loc[bd['IDTIPOSOLICITACAO'] == 46]
    count_cycle_9a = cycle_9a['IDSIGFI'].count()
    count_cycle_9a = np.int64(count_cycle_9a)
    count_cycle_9a = int(count_cycle_9a)
    delta_9a = count_cycle_9a - count_bdins
    delta_9a = np.int64(delta_9a)
    delta_9a = int(delta_9a)
    #Contagem por ciclos 10A
    cycle_10a = bd.loc[bd['IDTIPOSOLICITACAO'] == 47]
    count_cycle_10a = cycle_10a['IDSIGFI'].count()
    count_cycle_10a = np.int64(count_cycle_10a)
    count_cycle_10a = int(count_cycle_10a)
    delta_10a = count_cycle_10a - count_bdins
    delta_10a = np.int64(delta_10a)
    delta_10a = int(delta_10a)


    # Apresenta as tabelas
    st.subheader("Status de Execuções O&M 1ª Tranche Acre")
    #st.dataframe(bd)

    # st.subheader("Tabela de Instalações")
    #st.dataframe(bd_ins)
    # st.subheader("Quantidade de execuções O&M 1ª Tranche Acre")
    #st.write(count_bd)
    # st.subheader("Quantidade de Instalações")
    #st.write(count_bdins)
    
    # Criação de colunas para as métricas
    col1_title, col2_title = st.columns(2)
    
    col1_title.metric(label="Instalações 2ªTranche",value=count_bdins)
    col2_title.metric(label="Os 2ªTranche executados",value=count_oem)
    
    # Criação de colunas para as métricas de cada ciclo bloco 01
    col1_indicator_1a, col2_indicator_2a, col3_indicator_3a, col4_indicator_4a, col5_indicator_5a,  = st.columns(5)
    col1_indicator_1a.metric(label="Quant executada 1A",value=count_cycle_1a,delta=delta_1a)
    col2_indicator_2a.metric(label="Quant executada 2A",value=count_cycle_2a,delta=delta_2a)
    col3_indicator_3a.metric(label="Quant executada 3A",value=count_cycle_3a,delta=delta_3a)
    col4_indicator_4a.metric(label="Quant executada 4A",value=count_cycle_4a,delta=delta_4a)
    col5_indicator_5a.metric(label="Quant executada 5A",value=count_cycle_5a,delta=delta_5a)
    #Criação de colunas para as métricas de cada ciclo bloco 02
    col6_indicator_6a, col7_indicator_7a, col8_indicator_8a, col9_indicator_9a, col10_indicator_10a = st.columns(5)
    col6_indicator_6a.metric(label="Quant executada 6A",value=count_cycle_6a,delta=delta_6a)
    col7_indicator_7a.metric(label="Quant executada 7A",value=count_cycle_7a,delta=delta_7a)
    col8_indicator_8a.metric(label="Quant executada 8A",value=count_cycle_8a,delta=delta_8a)
    col9_indicator_9a.metric(label="Quant executada 9A",value=count_cycle_9a,delta=delta_9a)
    col10_indicator_10a.metric(label="Quant executada 10A",value=count_cycle_10a,delta=delta_10a)

# Chama a função principal
if __name__ == "__main__":
    base_oem_2t_ac()