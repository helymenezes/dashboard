import streamlit as st
import pandas as pd

def filter_oem():
    st.title('PRODUÇÃO ORDEM E MANUTENÇÃO')
    
    @st.cache_data
    def read_dataframe_oem():
        df_oem = pd.read_excel(r'C:\Users\helym\projeto_python\dashboard\content\base_sip_Concluido.xlsx')
        del_status = ['TREINAMENTO', 'CADASTRO', 'TREINAMENTO']
        del_user = ['MARCO', 'LUIZ.CARLOS']
        del_route = [55, 70]
        
        df_oem = df_oem[~df_oem['STATUS'].isin(del_status)]
        df_oem = df_oem[~df_oem['EXECUTOR'].isin(del_user)]
        df_oem = df_oem[~df_oem['ROTA'].isin(del_route)]
        
        df_oem[['NUMOS', 'IDSIGFI', 'UC']] = df_oem[['NUMOS', 'IDSIGFI', 'UC']].astype(str)
        
        return df_oem
    
    def application_filter(df, tipo_value, origem_value, data_inicial, data_final):
        df_filtered = df[
            df["TIPO"].isin(tipo_value) &
            df['ORIGEM'].isin(origem_value) &
            (df['DATACONCLUSAO'] >= data_inicial) &
            (df['DATACONCLUSAO'] <= data_final)
        ]
        return df_filtered
    
    # Apresenta a tabela do dataframe do streamlit e aplica o check box
    def show_sheet(df_filtered):
        df_filtered['CHECKBOX'] = ['FALSE'] * len(df_filtered)
        st.dataframe(df_filtered[['CHECKBOX', 'NUMOS', 'NUMOCORRENCIA', 'UC', 'IDSIGFI', 'TIPOCAUSA', 
                                'NOMECLIENTE', 'ROTA', 'STATUS', 'EXECUTOR', 'DTCONCLUSAO', 'LATLONCON','DESCADICIONALPROG']])
    
    # Carrega o dataframe para aplicação do filtro e joga ele na variável df.
    df = read_dataframe_oem()
    
    col01, col02 = st.columns(2)
    data_inicial_filter = pd.to_datetime(col01.date_input('Data Inicial: ', value = df['DATACONCLUSAO'].min()))
    #data_inicial_filter = col01.date_input('Data Inicial:', value=df['DTCONCLUSAO'].min())
    data_final_filter = pd.to_datetime(col02.date_input('Data Final: ', value = df['DATACONCLUSAO'].max()))
    #data_final_filter = col02.date_input('Data Final:', value=df['DTCONCLUSAO'].max())
    
    col_tipo, col_origem = st.columns(2)
    tipo_options = sorted(list(df['TIPO'].unique()))
    tipo_filter = col_tipo.multiselect("Tipo: ", tipo_options)
    
    origem_options = sorted(list(df['ORIGEM'].unique()))
    origem_filter = col_origem.multiselect("Origem: ",origem_options)
    
    # Button to execute the filter and display the table
    if st.button('Executar Filtros'):
        df_filtered = application_filter(df, tipo_filter, origem_filter, data_inicial_filter, data_final_filter)
        
        if df_filtered.empty:
            st.warning("Não foi encontrado o resultado pré-definido. Redefina os filtros e tente novamente")
        else:
            show_sheet(df_filtered)
