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

        # NEW: Next 버튼 추가 및 처리
        if st.button("Next"):
            st.write("Searching for genes in BioPortal...")

            gene_column = dataframe.columns[0]  # 첫 번째 열을 유전자 열로 간주
            gene_matches = []

            for gene in dataframe[gene_column]:
                search_url = f"{search_base_url}{gene}&apikey={Api}"
                search_response = requests.get(search_url)

                if search_response.status_code == 200:
                    search_results = search_response.json().get('collection', [])
                    if search_results:
                        for result in search_results[:1]:  # 각 유전자에 대해 상위 1개 결과만 표시
                            match = {
                                "Gene": gene,
                                "Matched Term": result.get('prefLabel', 'N/A'),
                                "Ontology": result.get('links', {}).get('ontology', 'N/A'),
                                "Definition": result.get('definition', ['No definition'])[0]  # 정의 표시
                            }
                            gene_matches.append(match)
                    else:
                        gene_matches.append({"Gene": gene, "Matched Term": "No Match Found", "Ontology": "N/A", "Definition": "N/A"})
                else:
                    st.error(f"Failed to search BioPortal for gene: {gene}")

            # 매칭 결과를 데이터프레임으로 표시
            matches_df = pd.DataFrame(gene_matches)
            st.write("### Gene Matches:")
            st.dataframe(matches_df)

            # CSV 파일로 저장 옵션 제공
            csv_matches = matches_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Gene Matches as CSV",
                data=csv_matches,
                file_name="gene_matches.csv",
                mime="text/csv"
            )

    else:
        st.error("Could not detect a suitable header row automatically.")
