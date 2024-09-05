import sys
import os

# Adiciona o caminho do diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from filters.ac import filter_com
from filters.mt import filter_com_mt
from filters.oem_mt import filter_oem_mt
from filters.oem import filter_oem

def main():
    st.sidebar.title('Menu')
    pages_operation = st.sidebar.selectbox('Operações', [
        'O&M-Lote1(Cruzeiro do SUl/AC)',
        'O&M-Lote2(Querência / MT)',
        'Comissionamento-2ªtranche-Lote1&2(Cruzeiro do sUl/Sena Madureira/AC)',
        'Comissionamento-2ªtranche-Lote2(Sorriso - MT)'
        
    ])

    if pages_operation == 'O&M-Lote1(Cruzeiro do SUl/AC)':
        filter_com()
    elif pages_operation == 'O&M-Lote2(Querência / MT)':
        filter_com_mt()
    elif pages_operation == 'Comissionamento-2ªtranche-Lote1&2(Cruzeiro do sUl/Sena Madureira/AC)':
        filter_oem_mt()
    elif pages_operation == 'Comissionamento-2ªtranche-Lote2(Sorriso - MT)':
        filter_oem()

if __name__ == "__main__":
    main()
