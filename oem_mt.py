import pandas as pd
import streamlit as st  
import plotly.express as px

import sys
import os

# Diretório atual (onde order.py está localizado)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Diretório pai (onde oem_mt.py está localizado)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Adiciona o diretório pai ao sys.path
sys.path.append(parent_dir)

def filter_oem_mt():
    st.title("PRODUÇÃO O&M MT")    

    @st.cache_data

    def ler_planilha():
        excluir_status = ['TREINAMENTO', 'CADASTRO', 'TREINAMENTO']
        excluir_usuario = ['LUIZ.CARLOS']
        excluir_rota = [600]
        df_bd = pd.read_excel(r"content\base_sip_Concluido_mt.xlsx")

        # Aplicar os filtros sequencialmente
        df = df_bd[~df_bd['STATUS'].isin(excluir_status)]
        df = df[~df['EXECUTOR'].isin(excluir_usuario)]
        df = df[~df['ROTA'].isin(excluir_rota)]

        # Converter apenas as colunas 'NUMOS' e 'IDSIGFI' para strings
        df[['NUMOS', 'IDSIGFI','UC']] = df[['NUMOS', 'IDSIGFI','UC']].astype('str')

        return df
    
    @st.cache_data
    def aplicar_filtros(df, rota_value, status_value, tipo_value, executor_value, data_inicial, data_final, etapa_value, tipocausa_value):
        """Aplica filtros a uma planilha."""
        df_filtered_oem_mt = df[
            df["ROTA"].isin(rota_value) &
            df["STATUS"].isin(status_value) &
            df["TIPO"].isin(tipo_value) &
            df["EXECUTOR"].isin(executor_value) &
            df["ORIGEM"].isin(etapa_value) &
            df["TIPOCAUSA"].isin(tipocausa_value) &
            (df["DTCONCLUSAO"] >= data_inicial) &
            (df["DTCONCLUSAO"] <= data_final)
        ]
        return df_filtered_oem_mt

    def gerar_grafico(df_filtered_oem_mt):
        """Gera um gráfico com base nos dados filtrados."""
        grafico = pd.pivot_table(df_filtered_oem_mt, values='NUMOS', index=['ROTA'], columns=['STATUS'], aggfunc='count')
        fig = px.bar(grafico, barmode='stack')
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=list(grafico.index), ticktext=list(grafico.index)))
        fig.update_layout(xaxis_title='ROTA', yaxis_title='CONTAGEM', hovermode='closest')
        fig.update_layout(height=800, width=1280)
        st.plotly_chart(fig)

    def mostrar_dataframe(df_filtered_oem_mt):
        """Mostra o DataFrame em formato de tabela."""
        # Adiciona uma coluna de checkboxes ao DataFrame
        df_filtered_oem_mt['Selecionar'] = [False] * len(df_filtered_oem_mt)

        # Exibe o DataFrame com a coluna de checkboxes
        st.dataframe(df_filtered_oem_mt[['Selecionar', 'NUMOS', 'NUMOCORRENCIA', 'UC', 'IDSIGFI', 'TIPOCAUSA', 
                                'NOMECLIENTE', 'ROTA', 'STATUS', 'EXECUTOR', 'DTCONCLUSAO', 'LATLONCON','DESCADICIONALPROG']])
        
        # Acessa o valor máximo da coluna "NUMOS"
        favorite_command = df_filtered_oem_mt["NUMOS"].max()
        st.markdown(f"Your favorite command is **{favorite_command}** 🎈")

        # Botão para armazenar dados filtrados
        if st.button("Armazenar Dados"):
            st.session_state['df_temp'] = df_filtered_oem_mt
            
    def mostrar_dataframe_2():
        column_mapping = {
            'NUMOS': 'Quant./Rota',
            'ROTA': 'Rota'
        }
        df_filtered_oem_mt.rename(columns=column_mapping, inplace = True )
        table_dinamic_mt = st.dataframe(pd.pivot_table(df_filtered_oem_mt,
                                                        values=['Quant./Rota'],
                                                        index=['STATUS'],
                                                        columns=['Rota'],
                                                        fill_value=0,
                                                        aggfunc={'Quant./Rota': 'count'},
                                                        margins=True,
                                                        margins_name='Total'),
                                        width=1000)
        
    def mostrar_dataframe_3():
        column_mapping_2 = {
            'NUMOS':'Quant./Usuário'
        }
        df_filtered_oem_mt.rename(columns=column_mapping_2, inplace = True )
        table_dinamic_mt = st.dataframe(pd.pivot_table(df_filtered_oem_mt,
                                                    values=['Quant./Usuário'],
                                                    index=['EXECUTOR'],
                                                    columns=['ROTA'],  # Alteração aqui
                                                    fill_value=0,
                                                    aggfunc={'Quant./Usuário':'count'},
                                                    margins=True,
                                                    margins_name='Total'))
    def mostrar_dataframe_4():
            column_mapping_3 = {
                'NUMOS':'Quant./Tipo O.S'
            }
            df_filtered_oem_mt.rename(columns=column_mapping_3, inplace = True )
            table_dinamic_mt = st.dataframe(pd.pivot_table(df_filtered_oem_mt,
                                                        values=['Quant./Tipo O.S'],
                                                        index=['TIPO'],
                                                        columns=['EXECUTOR'],  # Alteração aqui
                                                        fill_value=0,
                                                        aggfunc={'Quant./Tipo O.S':'count'},
                                                        margins=True,
                                                        margins_name='Total'))
    df = ler_planilha()
    df["DTCONCLUSAO"] = pd.to_datetime(df["DTCONCLUSAO"]).dt.date

    #Criando duas colunas para os seletores de data inicial e final:
    col1_dt, col2_dt = st.columns(2)
    data_inicial_filter = col1_dt.date_input("Data Inicial:", value=df["DTCONCLUSAO"].min(),key='data_inicial')
    data_final_filter = col2_dt.date_input("Data Final:", value=df["DTCONCLUSAO"].max(),key='data_final')
    # Criando duas colunas para caixa de opçoes curtas com origem e tipo
    col_origem, col_tipo = st.columns(2)
    origem_options = sorted(list(df['ORIGEM'].unique()))
    origem_filter = col_origem.multiselect("Origem:", origem_options)

    tipo_options = sorted(list(df['TIPO'].unique()))
    tipo_filter = col_tipo.multiselect("Tipo:", tipo_options)

    status_options = sorted(list(df['STATUS'].unique()))
    status_filter = st.multiselect("Status:", status_options)

    rota_options = sorted(list(df.loc[df['ROTA'].notna(), 'ROTA'].unique()))
    rota_check_all = st.checkbox("Selecionar todas Rotas")
    if rota_check_all:
        rota_filter = [value for value in rota_options if value != 'nan']
    else:
        rota_filter = st.multiselect("Rotas:", rota_options)
    
    executor_options = sorted(list(df.loc[df['EXECUTOR'].notna(), 'EXECUTOR'].unique()))
    executor_check_all = st.checkbox("Selecionar todos Executores")
    if executor_check_all:
        executor_filter = [value for value in executor_options if value != 'nan']
    else:
        executor_filter = st.multiselect("Usuário:", executor_options)

    tipocausa_options = sorted(list(df.loc[df['TIPOCAUSA'].notna(),'TIPOCAUSA'].unique()))
    tipocausa_check_all = st.checkbox("Selecionar todas as Causas")
    if tipocausa_check_all:
        tipocausa_filter = st.multiselect("Tipo Causa: ", tipocausa_options, default= tipocausa_options)
    else:
        tipocausa_filter = st.multiselect("Tipo Causa", tipocausa_options)
    
    df_filtered_oem_mt = aplicar_filtros(df, rota_filter, status_filter, tipo_filter, executor_filter, data_inicial_filter, data_final_filter, origem_filter, tipocausa_filter)

    # Crie duas colunas lado a lado
    col1, col2, col3, col4, col5 = st.columns(5)
    # Botão "Apresentar Tabela"
    if col1.button("Producão",key="producao_button"):
        if df_filtered_oem_mt.empty:
            st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
        else:
            mostrar_dataframe(df_filtered_oem_mt)

    # Botão "Apresentar Tabela Produção dia"
    if col3.button("St/Validação",key='validacao_button'):
        if df_filtered_oem_mt.empty:
            st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
        else:
            mostrar_dataframe_2()

    # Botão "Apresentar Tabela Produção status"
    if col4.button("Prod./Usuário",key='usuario_button'):
        if df_filtered_oem_mt.empty:
            st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
        else:
            mostrar_dataframe_3()

    # Botão "Apresentar Tabela Produção Tipo de OS"
    if col5.button("Prod./TIPO OS",key='os_button'):
        if df_filtered_oem_mt.empty:
            st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
        else:
            mostrar_dataframe_4()

    # Botão "Gerar Gráfico"
    if col2.button("Gerar Gráfico",key='grafico_button'):
        if df_filtered_oem_mt.empty:
            st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
        else:
            gerar_grafico(df_filtered_oem_mt)