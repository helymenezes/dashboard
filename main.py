import streamlit as st
import oem
import com_ac
import com_mt

st.sidebar.title('Menu')
pages_operation = st.sidebar.selectbox('Operações', [
    'O&M-1ªtranche-Lote1(Cruzeiro do SUl/AC)',
    'Comissonamento-2ªtranche-Lote1&2(Cruzeiro do sUl/Sena Madureira/AC)',
    'Comissonamento-2ªtranche-Lote3(Sorriso - MT)'
])

if pages_operation == 'O&M-1ªtranche-Lote1(Cruzeiro do SUl/AC)':
    oem.filter_oem()
if pages_operation == 'Comissonamento-2ªtranche-Lote1&2(Cruzeiro do sUl/Sena Madureira/AC)':
    com_ac.filter_com()
if pages_operation == 'Comissonamento-2ªtranche-Lote3(Sorriso - MT)':
    com_mt.filter_com_mt()