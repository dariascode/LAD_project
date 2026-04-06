import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data.load_data import load_data

st.set_page_config(page_title="Used Cars Dashboard", layout="wide")

st.title("Used Cars Interactive Dashboard")

# =====================
# LOAD DATA
# =====================

df = load_data()

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

# label for comparison
df["car_label"] = (
    df["brand"] + " " +
    df["model"] + " (" +
    df["year"].astype(int).astype(str) + ")"
)

# =====================
# SIDEBAR FILTERS
# =====================

year_min = int(df["year"].quantile(0.01))
year_max = int(df["year"].quantile(0.99))

price_min = int(df["price"].quantile(0.01))
price_max = int(df["price"].quantile(0.99))

mileage_min = int(df["mileage"].quantile(0.01))
mileage_max = int(df["mileage"].quantile(0.99))

st.sidebar.header("Filters")

brand_filter = st.sidebar.multiselect(
    "Brand",
    options=sorted(df["brand"].unique()),
    default=sorted(df["brand"].unique())
)

transmission_filter = st.sidebar.multiselect(
    "Transmission",
    options=df["transmission"].unique(),
    default=df["transmission"].unique()
)

year_range = st.sidebar.slider(
    "Year",
    year_min,
    year_max,
    (year_min, year_max)
)

price_range = st.sidebar.slider(
    "Price",
    price_min,
    price_max,
    (price_min, price_max)
)

mileage_range = st.sidebar.slider(
    "Mileage",
    mileage_min,
    mileage_max,
    (mileage_min, mileage_max)
)

filtered_df = df[
    (df["brand"].isin(brand_filter)) &
    (df["transmission"].isin(transmission_filter)) &
    (df["year"].between(year_range[0], year_range[1])) &
    (df["price"].between(price_range[0], price_range[1])) &
    (df["mileage"].between(mileage_range[0], mileage_range[1]))
]

# =====================
# TABS
# =====================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Visual Analysis",
    "Brand Comparison",
    "Dataset",
    "Custom Charts"
])

# =====================
# TAB 1 OVERVIEW
# =====================

with tab1:
    st.subheader("About the Dataset")

    st.markdown("""
    This dataset contains information about used cars from multiple brands such as Audi, BMW, Ford, Toyota, Volkswagen, Skoda, Mercedes, and Hyundai.

    It includes technical specifications and market data such as price, mileage, fuel type, and engine size.

    The dataset is used to analyze relationships between car characteristics and their market value.
    """)
    st.subheader("Variables Description")

    st.markdown("""
    - **brand** — car manufacturer (e.g. Audi, BMW, Toyota)  
    - **model** — specific car model (e.g. A3, Focus, Corolla)  
    - **year** — year of production  
    - **price** — price of the car  
    - **transmission** — type of transmission (Manual / Automatic)  
    - **mileage** — total distance driven  
    - **fuelType** — fuel type (Petrol / Diesel / Hybrid)  
    - **tax** — vehicle tax  
    - **mpg** — fuel efficiency (miles per gallon)  
    - **engineSize** — engine size (liters)  
    - **car_age** — age of the car (calculated feature)  
    - **mileage_per_year** — average mileage per year  
    - **price_per_year** — price adjusted by age  
    """)

    st.subheader("Dataset Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Cars", len(filtered_df))
    col2.metric("Average Price", int(filtered_df["price"].mean()))
    col3.metric("Average Mileage", int(filtered_df["mileage"].mean()))

    st.subheader("Top 10 Most Expensive Cars")

    top10 = filtered_df.sort_values("price", ascending=False).head(10)

    st.dataframe(top10)



# =====================
# TAB 5 CUSTOM CHARTS
# =====================

with tab5:

    st.subheader("Create Your Own Chart")

    chart_type = st.selectbox(
        "Chart type",
        ["Scatter", "Histogram", "Boxplot", "Bar chart"]
    )

    numeric_columns = filtered_df.select_dtypes(include="number").columns
    categorical_columns = filtered_df.select_dtypes(exclude="number").columns

    x_axis = st.selectbox("X axis", filtered_df.columns)

    if chart_type in ["Scatter", "Boxplot", "Bar chart"]:
        y_axis = st.selectbox("Y axis", numeric_columns)
    else:
        y_axis = None

    color = st.selectbox(
        "Color by",
        ["None"] + list(categorical_columns)
    )

    fig, ax = plt.subplots(figsize=(6,4))

    if chart_type == "Scatter":

        sns.scatterplot(
            data=filtered_df,
            x=x_axis,
            y=y_axis,
            hue=None if color == "None" else color,
            ax=ax
        )

    elif chart_type == "Histogram":

        sns.histplot(
            data=filtered_df,
            x=x_axis,
            hue=None if color == "None" else color,
            bins=30,
            ax=ax
        )

    elif chart_type == "Boxplot":

        sns.boxplot(
            data=filtered_df,
            x=x_axis,
            y=y_axis,
            ax=ax
        )

    elif chart_type == "Bar chart":

        temp = filtered_df.groupby(x_axis)[y_axis].mean().reset_index()

        sns.barplot(
            data=temp,
            x=x_axis,
            y=y_axis,
            ax=ax
        )

    ax.set_title("Custom Chart")

    st.pyplot(fig)