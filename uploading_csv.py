# import streamlit as st
# import pandas as pd
# import openpyxl
# import xlrd

# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
#     dataframe = pd.read_csv(uploaded_file)
#     st.write(dataframe)
# elif uploaded_file is not None:
#     dataframe = pd.read_excel(uploaded_file)
#     st.write(dataframe)


import streamlit as st
import pandas as pd
import openpyxl
import xlrd

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        dataframe = pd.read_csv(uploaded_file, header=None)  # 헤더 없이 읽기
    else:
        dataframe = pd.read_excel(uploaded_file, header=None)  # 헤더 없이 읽기

    # 헤더 행 자동 탐지 (모든 열이 문자열로 채워진 첫 번째 행을 헤더로 간주)
    header_row_index = None
    for index, row in dataframe.iterrows():
        if row.notna().all():  # 모든 값이 비어있지 않다면 헤더로 간주
            header_row_index = index
            break

    if header_row_index is not None:
        # 선택된 행을 헤더로 재설정
        if uploaded_file.name.endswith('.csv'):
            dataframe = pd.read_csv(uploaded_file, header=header_row_index)
        else:
            dataframe = pd.read_excel(uploaded_file, header=header_row_index)

        st.write(dataframe)
    else:
        st.error("Could not detect a suitable header row automatically.")
