import streamlit as st
# Importa os módulos necessários
import oem
import oem_mt
import com_ac
import com_mt
from pages import maps


st.sidebar.title('Menu')
# Menu de seleção para operações
pages_operation = st.sidebar.selectbox('Operações', [
    'O&M-Lote1(Cruzeiro do SUl/AC)',
    'O&M-Lote3(Querência / MT)',
    'Comissionamento-2ªtranche-Lote1&2(Cruzeiro do sUl/Sena Madureira/AC)',
    'Comissionamento-2ªtranche-Lote3(Sorriso - MT)'
])

# Condicional baseado na seleção do menu
if pages_operation == 'O&M-Lote1(Cruzeiro do SUl/AC)':
    oem.filter_oem()
elif pages_operation == 'Comissionamento-2ªtranche-Lote1&2(Cruzeiro do sUl/Sena Madureira/AC)':
    com_ac.filter_com()
elif pages_operation == 'Comissionamento-2ªtranche-Lote3(Sorriso - MT)':
    com_mt.filter_com_mt()
elif pages_operation == 'O&M-Lote3(Querência / MT)':
    oem_mt.filter_oem_mt()