import streamlit as st
import pandas as pd
import openpyxl
import xlrd

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    dataframe = pd.read_excel(uploaded_file)
    st.write(dataframe)
elif uploaded_file is not None:
    dataframe = pd.read_excel(uploaded_file)
    st.write(dataframe)