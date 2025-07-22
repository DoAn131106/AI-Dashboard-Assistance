import streamlit as st
import pandas as pd
from query_parser import parse_query

# Load your sample Power BI dataset (Excel or CSV)
df = pd.read_excel("data/sample_data.xlsx")  # or pd.read_csv(...)

st.set_page_config(page_title="AI Dashboard Assistant")
st.title("AI Dashboard Assistant")

query = st.text_input("Ask a question about your data:")

if query:
    parsed = parse_query(query)
    st.write("🔍 Parsed Query:", parsed)

    # Basic filtering logic (initial version)
    data = df.copy()

    # Example: filter by year/quarter if 'filters' contain dates
    for f in parsed["filters"]:
        if "2024" in f:
            data = data[data["year"] == 2024]
        if "q2" in f.lower():
            data = data[data["quarter"] == "Q2"]

    # Show chart if metric is valid
    if parsed["metrics"] and parsed["dimensions"]:
        metric = parsed["metrics"][0]
        dimension = parsed["dimensions"][0]

        grouped = data.groupby(dimension)[metric].sum().reset_index()
        st.bar_chart(grouped, x=dimension, y=metric)
    else:
        st.warning("Couldn't find both a metric and a dimension in your query.")
