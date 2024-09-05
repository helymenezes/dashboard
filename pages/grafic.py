import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df.fillna(0, inplace=True)
    df.reset_index(inplace=True)  # Resetar o índice aqui para criar as colunas level_x
    return df

def preprocess_data(df):
    # Após resetar o índice, essas colunas estarão disponíveis
    try:
        df['Col_1'] = df['level_0'].astype(str) + ',' + df['level_1'].astype(str)
        df['Col_2'] = df['level_2'].astype(str) + ',' + df['level_3'].astype(str)
        df['Col_3'] = df['Days Ago'].astype(str) + ',' + df['Min Battery Volt.(V)'].astype(str)
        df['Col_4'] = df['Max Battery Volt.(V)'].astype(str) + ',' + df['Max Charge Curr.(A)'].astype(str)
        df['Col_5'] = df['Discharge Ah'].astype(str) + ',' + df['Charge KWh'].astype(str)
        df['Col_6'] = df['Max Discharge Curr.(A)'].astype(int) / 1000
        #df['Indicador']= indicador

        # Remover colunas originais que não são mais necessárias
        df = df.drop(['level_0', 'level_1', 'level_2', 'level_3','level_4','Days Ago', 'Min Battery Volt.(V)', 
                      'Max Battery Volt.(V)', 'Max Charge Curr.(A)', 'Charge KWh', 'Discharge Ah'], axis=1)
        df = df.rename(columns={'level_0':'Ciclo','Max Discharge Curr.(A)':'Carga Max.(W)','Col_1':'Bateria Min.(V)',
                               'Col_2':'Bateria Max.(V)','Col_3':'Corrente Max(A)Carg.','Col_4':'Corrente Max(A)Descarg',
                               'Col_5':'Carga KWh','Max Charge Power(W)':'Descarga Ah','Max Discharge Power(W)':'Carga Ah',
                               'Charge Ah':'Descarga Max(W)','Col_6':'ConversãoCarga Max(W /KW)'})
        #Aplicação de ciclos:
        #dtconclusion = pd.to_datetime(result['DTCONCLUSAO'])
        # ocurrence = base_oem_1t_ac()

        # initial_days_ago = df['Ciclo'].iloc[0]  # Use 'result' em vez de 'datalog' para pegar o valor correto
        # df['Data'] = pd.date_range(end=dtconclusion.iloc[0], periods=initial_days_ago + 1, freq='D')
        # df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')  # Use 'dt' para acessar métodos de datetime

        return df
    except Exception as e:
        st.error(f"Erro ao processar os dados: {str(e)}")
        return None

def plot_graph(df):
    if df is not None:
        fig, ax = plt.subplots(figsize=(18, 10))
        ax.plot(df['Ciclo'], df['Bateria Min.(V)'], label='Bateria Mínima (V)')
        ax.legend()
        st.pyplot(fig)

def main():
    st.title('Visualizador de Dados com Streamlit')
    
    uploaded_file = st.file_uploader("Carregar arquivo CSV", type="csv")
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        if st.button('Processar Dados'):
            processed_data = preprocess_data(data)
            if processed_data is not None:
                st.write(processed_data)
        if st.button('Gerar Gráfico'):
            plot_graph(processed_data)

if __name__ == '__main__':
    main()
