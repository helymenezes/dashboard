import pandas as pd     
import streamlit  as st 
import sys
import os
import oem_mt import filter_oem_mt

# Diretório atual (onde order.py está localizado)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Diretório pai (onde oem_mt.py está localizado)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Adiciona o diretório pai ao sys.path
sys.path.append(parent_dir)

base_geral_oem_mt = filter_oem_mt

# Removendo os STATUS 'CANCELADO','NAO CONFORME','TREINADO'
excluirstatus = ['CANCELADO','DUPLICADO','TREINAMENTO']

base_geral_oem_mt = base_geral_oem_mt.drop(base_geral_oem_mt[(base_geral_oem_mt['STATUS'].str.contains('|'.join(excluirstatus))) |
                         (base_geral_oem_mt['STATUS'].str.contains('|'.join(excluirstatus))) |
                         (base_geral_oem_mt['STATUS'].str.contains('|'.join(excluirstatus))) |
                         (base_geral_oem_mt['STATUS'].str.contains('|'.join(excluirstatus))) |
                         (base_geral_oem_mt['STATUS'].str.contains('|'.join(excluirstatus)))].index)


#base_geral_oem_mt[['TIPOCAUSA']] = base_geral_oem_mt.astype('str')
base_geral_oem_mt[['TIPOCAUSA']]






