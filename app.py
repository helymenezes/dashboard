import pandas as pd
import locale
from datetime import datetime
from numpy.core.fromnumeric import size
import streamlit as st  
import plotly.express as px


st.sidebar.title('MENU')
Page_operation = st.sidebar.selectbox('Operações', ['O&M-1ªtranche-Lote1(Cruzeiro do SUl - AC)',
                                                    'Comissonamento-2ªtranche-Lote1&2(Cruzeiro do sUl/Sena Madureira - AC)',
                                                    'Comissonamento-2ªtranche-Lote3(Sorriso - MT)'])


#Gráfico e tabela  O&M 2ª Tranche lote 01:
if Page_operation == 'O&M-1ªtranche-Lote1(Cruzeiro do SUl - AC)':
    st.title("PRODUÇÃO O&M")    

    @st.cache_data

    def ler_planilha():
        excluir_status = ['TREINAMENTO', 'CADASTRO', 'TREINAMENTO']
        excluir_usuario = ['MARCO', 'LUIZ.CARLOS']
        excluir_rota = [70, 55]
        df_bd = pd.read_excel(r"C:\Users\HELY-DELL\projetos_python\dashboard\content\base_sip_Concluido.xlsx")

        # Aplicar os filtros sequencialmente
        df = df_bd[~df_bd['STATUS'].isin(excluir_status)]
        df = df[~df['EXECUTOR'].isin(excluir_usuario)]
        df = df[~df['ROTA'].isin(excluir_rota)]

        # Converter apenas as colunas 'NUMOS' e 'IDSIGFI' para strings
        df[['NUMOS', 'IDSIGFI','UC']] = df[['NUMOS', 'IDSIGFI','UC']].astype('str')

        return df
    
    @st.cache_data
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
        fig.update_layout(height=800, width=1280)
        st.plotly_chart(fig)

    def mostrar_dataframe(df_filtered):
        """Mostra o DataFrame em formato de tabela."""
        # Adiciona uma coluna de checkboxes ao DataFrame
        df_filtered['Selecionar'] = [False] * len(df_filtered)

        # Exibe o DataFrame com a coluna de checkboxes
        st.dataframe(df_filtered[['Selecionar', 'NUMOS', 'NUMOCORRENCIA', 'UC', 'IDSIGFI', 'TIPOCAUSA', 
                                'NOMECLIENTE', 'ROTA', 'STATUS', 'EXECUTOR', 'DTCONCLUSAO', 'LATLONCON']])
        
        # Acessa o valor máximo da coluna "NUMOS"
        favorite_command = df_filtered["NUMOS"].max()
        st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
        
    if __name__ == "__main__":
        df = ler_planilha()
        df["DTCONCLUSAO"] = pd.to_datetime(df["DTCONCLUSAO"]).dt.date

        # Configurando data com lib python Locale:
        locale.setlocale(locale.LC_TIME,'pt_BR.UTF-8')
        #Criando duas colunas para os seletores de data inicial e final:
        col1_dt, col2_dt = st.columns(2)
        data_inicial_filter = col1_dt.date_input("Data Inicial:", value=df["DTCONCLUSAO"].min())
        data_final_filter = col2_dt.date_input("Data Final:", value=df["DTCONCLUSAO"].max())
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
        
        df_filtered = aplicar_filtros(df, rota_filter, status_filter, tipo_filter, executor_filter, data_inicial_filter, data_final_filter, origem_filter)

        # Crie duas colunas lado a lado
        col1, col2 = st.columns(2)
        # Botão "Apresentar Tabela"
        if col1.button("Apresentar Tabela"):
            if df_filtered.empty:
                st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
            else:
                mostrar_dataframe(df_filtered)
        # Botão "Gerar Gráfico"
        if col2.button("Gerar Gráfico"):
            if df_filtered.empty:
                st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
            else:
                gerar_grafico(df_filtered)

#Gráfico e tabela  Comissionamento 2ª Tranche lote 01 & Lote 02:

if Page_operation == 'Comissonamento-2ªtranche-Lote1&2(Cruzeiro do sUl/Sena Madureira - AC)':
    st.title("COMISSIONAMENTOS LOTE 01 & 02")    

    @st.cache_data
    def ler_planilha():
        """Lê uma planilha do Excel."""
        excluir_status = ['TREINAMENTO', 'CADASTRO', 'TREINAMENTO']
        excluir_usuario = ['LUIZ.CARLOS']
        excluir_rota = [55, 70]
        df_bd = pd.read_excel(r"C:\Users\HELY-DELL\projetos_python\dashboard\content\base_sip_instalacoes_Geral_ac.xlsx")
        df = df_bd[~df_bd['STATUS'].isin(excluir_status)]
        df = df[~df['USUARIO'].isin(excluir_usuario)]
        df = df[~df['ROTA'].isin(excluir_rota)]
        return df

    @st.cache_data
    def aplicar_filtros(df, rota_value, status_value, tipo_value, usuario_value, data_inicial, data_final, etapa_value):
        """Aplica filtros a uma planilha."""
        df_filtered = df[
            df["ROTA"].isin(rota_value) &
            df["STATUS"].isin(status_value) &
            df["TIPO"].isin(tipo_value) &
            df["USUARIO"].isin(usuario_value) &
            df["ETAPA"].isin(etapa_value) &
            (df["CONCLUSAO"] >= data_inicial) &
            (df["CONCLUSAO"] <= data_final)
        ]
        return df_filtered

    def gerar_grafico(df_filtered):
        """Gera um gráfico com base nos dados filtrados."""
        grafico = pd.pivot_table(df_filtered, values='IDSERVICOSCONJ', index=['ROTA'], columns=['STATUS'], aggfunc='count')
        fig = px.bar(grafico, barmode='stack')
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=list(grafico.index), ticktext=list(grafico.index)))
        fig.update_layout(xaxis_title='ROTA', yaxis_title='CONTAGEM', hovermode='closest')
        fig.update_layout(height=800, width=1280)
        st.plotly_chart(fig)

    def mostrar_dataframe(df_filtered):
        """Mostra o DataFrame em formato de tabela."""
        # Adiciona uma coluna de checkboxes ao DataFrame
        df_filtered['Selecionar'] = [False] * len(df_filtered)

        # Exibe o DataFrame com a coluna de checkboxes
        st.dataframe(df_filtered[['Selecionar','IDSERVICOSCONJ','ROTA','CONCLUSAO','STATUS','USUARIO',
                                  'NOMEDOCLIENTE','OBSERVACAOINT','LATLONCONF','ENDERECO','MUNICIPIO','ETAPA','USUARIOALT']])
        
        # Acessa o valor máximo da coluna "IDSERVICOSCONJ"
        favorite_command = df_filtered["IDSERVICOSCONJ"].max()
        st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
        
    if __name__ == "__main__":
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

        df_filtered = aplicar_filtros(df, rota_filter, status_filter, tipo_filter, usuario_filter, data_inicial_filter, data_final_filter, etapa_filter)

        # Crie duas colunas lado a lado
        col1, col2 = st.columns(2)
        # Botão "Apresentar Tabela"
        if col1.button("Apresentar Tabela"):
            if df_filtered.empty:
                st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
            else:
                mostrar_dataframe(df_filtered)
        # Botão "Gerar Gráfico"
        if col2.button("Gerar Gráfico"):
            if df_filtered.empty:
                st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
            else:
                gerar_grafico(df_filtered)

#Gráfico e tabela  Comissionamento 2ª Tranche lote 03:

if Page_operation == 'Comissonamento-2ªtranche-Lote3(Sorriso - MT)':
    st.title("COMISSIONAMENTOS LOTE 03")    

    @st.cache_data
    def ler_planilha():
        """Lê uma planilha do Excel."""
        excluir_status = ['TREINAMENTO', 'CADASTRO', 'TREINAMENTO']
        excluir_usuario = ['LUIZ.CARLOS']
        excluir_rota = [55, 70]
        df_bd = pd.read_excel(r"C:\Users\HELY-DELL\projetos_python\dashboard\content\base_sip_instalacoes_Geral_mt.xlsx")
        df = df_bd[~df_bd['STATUS'].isin(excluir_status)]
        df = df[~df['USUARIO'].isin(excluir_usuario)]
        df = df[~df['ROTA'].isin(excluir_rota)]
        return df

    @st.cache_data
    def aplicar_filtros(df, rota_value, status_value, tipo_value, usuario_value, data_inicial, data_final, etapa_value):
        """Aplica filtros a uma planilha."""
        df_filtered = df[
            df["ROTA"].isin(rota_value) &
            df["STATUS"].isin(status_value) &
            df["TIPO"].isin(tipo_value) &
            df["USUARIO"].isin(usuario_value) &
            df["ETAPA"].isin(etapa_value) &
            (df["CONCLUSAO"] >= data_inicial) &
            (df["CONCLUSAO"] <= data_final)
        ]
        return df_filtered

    def gerar_grafico(df_filtered):
        """Gera um gráfico com base nos dados filtrados."""
        grafico = pd.pivot_table(df_filtered, values='IDSERVICOSCONJ', index=['ROTA'], columns=['STATUS'], aggfunc='count')
        fig = px.bar(grafico, barmode='stack')
        fig.update_layout(xaxis=dict(tickmode='array', tickvals=list(grafico.index), ticktext=list(grafico.index)))
        fig.update_layout(xaxis_title='ROTA', yaxis_title='CONTAGEM', hovermode='closest')
        fig.update_layout(height=800, width=1280)
        st.plotly_chart(fig)

    def mostrar_dataframe(df_filtered):
        """Mostra o DataFrame em formato de tabela."""
        # Adiciona uma coluna de checkboxes ao DataFrame
        df_filtered['Selecionar'] = [False] * len(df_filtered)

        # Exibe o DataFrame com a coluna de checkboxes
        st.dataframe(df_filtered[['Selecionar','IDSERVICOSCONJ','ROTA','CONCLUSAO','STATUS','USUARIO',
                                  'NOMEDOCLIENTE','OBSERVACAOINT','LATLONCONF','ENDERECO','MUNICIPIO','ETAPA','USUARIOALT']])
        
        # Acessa o valor máximo da coluna "IDSERVICOSCONJ"
        favorite_command = df_filtered["IDSERVICOSCONJ"].max()
        st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
        
    if __name__ == "__main__":
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
        rota_check_all = st.checkbox("Selecionar todas Rotas")

        if rota_check_all:
            rota_filter = st.multiselect("Rotas:", rota_options, default=rota_options)
        else:
            rota_filter = st.multiselect("Rotas:", rota_options)

        usuario_options = sorted(list(df.loc[df['USUARIO'].notna(),'USUARIO'].unique()))
        usuario_check_all = st.checkbox("Selecionar todos Executores")

        if usuario_check_all:
            usuario_filter = st.multiselect("Usuário:", usuario_options, default=usuario_options)
        else:
            usuario_filter = st.multiselect("Usuário:", usuario_options)

        df_filtered = aplicar_filtros(df, rota_filter, status_filter, tipo_filter, usuario_filter, data_inicial_filter, data_final_filter, etapa_filter)

        # Crie duas colunas lado a lado
        col1, col2 = st.columns(2)
        # Botão "Apresentar Tabela"
        if col1.button("Apresentar Tabela"):
            if df_filtered.empty:
                st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
            else:
                mostrar_dataframe(df_filtered)
        # Botão "Gerar Gráfico"
        if col2.button("Gerar Gráfico"):
            if df_filtered.empty:
                st.warning("Nenhum resultado encontrado. Refine os filtros e tente novamente.")
            else:
                gerar_grafico(df_filtered)

# Personalização de cor primaria hexagonal - #feb274
# Personalização de cor segundaria hexagonal - #3974b8
