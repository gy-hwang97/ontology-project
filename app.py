import streamlit as st
import pandas as pd
import plotly.express as px

# 초기화
if "data" not in st.session_state:
    st.session_state["data"] = []

# 입력 폼
with st.sidebar:
    st.header("Add New Expense")
    item = st.text_input("What did you buy?")
    price = st.number_input("Price:", min_value=0, value=0, step=1)
    if st.button("Add"):
        if item and price > 0:
            st.session_state["data"].append({"Item": item, "Price": price})

# 데이터 준비
df = pd.DataFrame(st.session_state["data"])

# 수정 기능
if not df.empty:
    st.sidebar.header("Edit Expense")
    # 수정할 항목 선택
    selected_item = st.sidebar.selectbox("Select an item to edit:", df["Item"])
    new_price = st.sidebar.number_input("New Price:", min_value=0, value=0, step=1)
    if st.sidebar.button("Update"):
        for entry in st.session_state["data"]:
            if entry["Item"] == selected_item:
                entry["Price"] = new_price
        st.sidebar.success(f"Updated {selected_item} to {new_price}.")

# 레이아웃 구성
col1, col2 = st.columns([1, 1])  # 왼쪽: 표, 오른쪽: 파이차트

# 왼쪽: 데이터 표
with col1:
    st.subheader("Expense Table")
    if not df.empty:
        st.table(df)
    else:
        st.write("No expenses added yet.")

# 오른쪽: 파이차트
with col2:
    st.subheader("Expense Chart")
    if not df.empty:
        fig = px.pie(df, names="Item", values="Price", title="Expense Distribution")
        st.plotly_chart(fig)
    else:
        st.write("Add expenses to see the chart.")
