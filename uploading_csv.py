import streamlit as st
import pandas as pd
import openpyxl
import xlrd
import requests

# API 키 및 URL 설정
Api = "6991b022-b43e-44b3-bf2e-650474fd5794"
search_base_url = "https://data.bioontology.org/search?q="

# 파일 업로드
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        dataframe = pd.read_csv(uploaded_file, header=None)
    else:
        dataframe = pd.read_excel(uploaded_file, header=None)

    # 헤더 행 자동 탐지
    header_row_index = None
    for index, row in dataframe.iterrows():
        if row.notna().all():
            header_row_index = index
            break

    if header_row_index is not None:
        # 선택된 행을 헤더로 재설정
        if uploaded_file.name.endswith('.csv'):
            dataframe = pd.read_csv(uploaded_file, header=header_row_index)
        else:
            dataframe = pd.read_excel(uploaded_file, header=header_row_index)

        st.write("### Uploaded File Preview")
        st.write(dataframe)

        # 열 선택 드롭다운
        selected_column = st.selectbox("Select Column", list(dataframe.columns))
        
        if selected_column:
            # 선택된 열의 고유 값들을 드롭다운으로 표시
            unique_values = dataframe[selected_column].unique()
            selected_value = st.selectbox(
                f"Select value from {selected_column}",
                unique_values
            )
            
            # 선택된 값에 대한 온톨로지 검색
            if selected_value and st.button("Search Ontology"):
                search_url = f"{search_base_url}{selected_value}&apikey={Api}"
                search_response = requests.get(search_url)
                
                if search_response.status_code == 200:
                    results = search_response.json().get('collection', [])
                    if results:
                        st.write(f"### Ontology matches for '{selected_value}':")
                        for result in results[:5]:  # 상위 5개 결과 표시
                            st.write("---")
                            st.write(f"Term: {result.get('prefLabel', 'N/A')}")
                            st.write(f"Ontology: {result.get('links', {}).get('ontology', 'N/A')}")
                            st.write(f"Definition: {result.get('definition', ['No definition'])[0]}")
                    else:
                        st.write(f"No ontology matches found for '{selected_value}'")
                else:
                    st.error(f"Failed to search BioPortal for value: {selected_value}")

    else:
        st.error("Could not detect a suitable header row automatically.")
