import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from pages.bipy.oembi import app_resume
from pages.bipy.oem_1t_ac import base_oem_1t_ac
from pages.bipy.oem_2t_ac_hoppecke import base_oem_2t_ac_hoppecke
from pages.bipy.oem_2t_ac import base_oem_2t_ac
from pages.bipy.oem_2t_mt import base_oem_2t_mt


def bi():
    st.sidebar.title('Opções B.I')
    pages_operation = st.sidebar.selectbox('Tranche', [
        'O&M-Resumo',
        'O&M-Lote1(Cruzeiro do SUl/AC)',
        'O&M-Lote2(Cruzeiro do Sul/AC)',
        'O&M-Lote2(Sena Madureira/AC)',
        'O&M-Lote2(Querência / MT)'
    ])

    if pages_operation == 'O&M-Resumo':
        app_resume()  # Chama a função app_oem diretamente, sem depender do botão
    elif pages_operation == 'O&M-Lote1(Cruzeiro do SUl/AC)':
        base_oem_1t_ac()
    elif pages_operation == 'O&M-Lote2(Cruzeiro do Sul/AC)':
        base_oem_2t_ac()
    elif pages_operation == 'O&M-Lote2(Sena Madureira/AC)':
        base_oem_2t_ac_hoppecke()
    elif pages_operation == 'O&M-Lote2(Querência / MT)':
        base_oem_2t_mt()

if __name__ == "__main__":
    bi()
