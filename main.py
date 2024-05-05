import streamlit as st
# Importa os módulos necessários
import oem
import com_ac
import com_mt



st.sidebar.title('Menu')
# Menu de seleção para operações
pages_operation = st.sidebar.selectbox('Operações', [
    'O&M-1ªtranche-Lote1(Cruzeiro do SUl/AC)',
    'Comissionamento-2ªtranche-Lote1&2(Cruzeiro do sUl/Sena Madureira/AC)',
    'Comissionamento-2ªtranche-Lote3(Sorriso - MT)'
])

# Condicional baseado na seleção do menu
if pages_operation == 'O&M-1ªtranche-Lote1(Cruzeiro do SUl/AC)':
    oem.filter_oem()
elif pages_operation == 'Comissionamento-2ªtranche-Lote1&2(Cruzeiro do sUl/Sena Madureira/AC)':
    com_ac.filter_com()
elif pages_operation == 'Comissionamento-2ªtranche-Lote3(Sorriso - MT)':
    com_mt.filter_com_mt()
    