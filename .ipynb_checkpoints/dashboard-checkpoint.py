import streamlit as st
from src.load_data import load_car_data

st.set_page_config(page_title="Car Market Analysis", layout="wide")

st.title("Car Market Analysis Dashboard")
st.markdown("This dashboard displays the cleaned car dataset.")

df = load_car_data()

if not df.empty:
    st.success("Data loaded successfully!")
    
    st.subheader("Data Preview (Cleaned Dataset)")
    st.dataframe(df)
    
    # add charts and filters here later
else:
    st.error("Failed to load data. Check if 'cars_cleaned_dataset.csv' is actually in the 'data/' folder.")