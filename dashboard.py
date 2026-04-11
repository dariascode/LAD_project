import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.load_data import load_car_data

st.set_page_config(page_title="Used Cars Dashboard", layout="wide")

st.title("Used Cars Interactive Dashboard")

# =====================
# LOAD DATA
# =====================

df = load_car_data()

if df.empty:
    st.error("Failed to load data. Check if 'cars_cleaned_dataset.csv' is inside the 'data/' folder.")
    st.stop()

df["brand"] = df["brand"].replace({
    "merc": "mercedes",
    "hyundi": "hyundai",
    "vw": "volkswagen"
})

current_year = 2026

df["car_age"] = current_year - df["year"]
df["car_age"] = df["car_age"].replace(0, 1)

df["mileage_per_year"] = df["mileage"] / df["car_age"]
df["price_per_year"] = df["price"] / df["car_age"]

df["car_label"] = (
    df["brand"] + " " +
    df["model"] + " (" +
    df["year"].astype(int).astype(str) + ")"
)

# =====================
# SIDEBAR FILTERS
# =====================
st.sidebar.header("🔍 Filters")

year_min = int(df["year"].quantile(0.01))
year_max = int(df["year"].quantile(0.99))

price_min = int(df["price"].quantile(0.01))
price_max = int(df["price"].quantile(0.99))

mileage_min = int(df["mileage"].quantile(0.01))
mileage_max = int(df["mileage"].quantile(0.99))

selected_years = st.sidebar.slider("Year Range", year_min, year_max, (2013, 2023))
selected_price = st.sidebar.slider("Price Range", price_min, price_max, (3111, 50000))
selected_mileage = st.sidebar.slider("Mileage Range", mileage_min, mileage_max, (5200, 100000))

selected_brands = st.sidebar.multiselect("Brand", df["brand"].unique(), default=["mercedes"])
selected_fuels = st.sidebar.multiselect("Fuel Type", df["fuelType"].unique(), default=["Diesel"])
selected_trans = st.sidebar.multiselect("Transmission", df["transmission"].unique(), default=["Semi-Auto", "Automatic"])

mask = (
    (df["year"] >= selected_years[0]) & (df["year"] <= selected_years[1]) &
    (df["price"] >= selected_price[0]) & (df["price"] <= selected_price[1]) &
    (df["mileage"] >= selected_mileage[0]) & (df["mileage"] <= selected_mileage[1]) &
    (df["brand"].isin(selected_brands)) &
    (df["fuelType"].isin(selected_fuels)) &
    (df["transmission"].isin(selected_trans))
)

filtered_df = df[mask]
st.success(f"Displaying {len(filtered_df)} out of {len(df)} vehicles.")

# =====================
# INTERACTIVE CHARTS
# =====================
st.subheader("📊 Build Your Own Chart")

chart_type = st.selectbox(
    "Chart type",
    ["Scatter", "Histogram", "Boxplot", "Bar chart"]
)

numeric_columns = filtered_df.select_dtypes(include="number").columns
categorical_columns = filtered_df.select_dtypes(exclude="number").columns

col1, col2, col3 = st.columns(3)
with col1:
    x_axis = st.selectbox("X axis", filtered_df.columns)

with col2:
    if chart_type in ["Scatter", "Boxplot", "Bar chart"]:
        y_axis = st.selectbox("Y axis", numeric_columns)
    else:
        y_axis = None

with col3:
    color = st.selectbox("Color by", ["None"] + list(categorical_columns))

fig, ax = plt.subplots(figsize=(10, 6))

try:
    if chart_type == "Scatter":
        sns.scatterplot(
            data=filtered_df, 
            x=x_axis, 
            y=y_axis, 
            hue=None if color == "None" else color, 
            alpha=0.6,  # Transparency to fix overplotting
            s=25,       # Smaller dot size for readability
            ax=ax
        )
    elif chart_type == "Histogram":
        sns.histplot(
            data=filtered_df, 
            x=x_axis, 
            hue=None if color == "None" else color, 
            bins=30, 
            alpha=0.7,
            ax=ax
        )
    elif chart_type == "Boxplot":
        sns.boxplot(
            data=filtered_df, 
            x=x_axis, 
            y=y_axis, 
            hue=None if color == "None" else color, 
            ax=ax
        )
    elif chart_type == "Bar chart":
        temp = filtered_df.groupby(x_axis)[y_axis].mean().reset_index()
        sns.barplot(data=temp, x=x_axis, y=y_axis, ax=ax)
        plt.xticks(rotation=45)

    st.pyplot(fig)
except Exception as e:
    st.error(f"Cannot generate chart with these parameters: {e}")

# =====================
# TAB 4 DATASET
# =====================

with tab4:

    st.subheader("Filtered Dataset")

    st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download filtered data",
        csv,
        "filtered_cars.csv",
        "text/csv"
    )