import streamlit as st
import pandas as pd
import plotly.express as px

# Loading data
df = pd.read_csv('cleaned_vehicles_us.csv')

# Converting 'cylinders' column to numeric, coercing errors 
df['cylinders'] = pd.to_numeric(df['cylinders'], errors='coerce')

# Applying the fillna with the median per 'model' group
df['cylinders'] = df.groupby('model')['cylinders'].transform(lambda x: x.fillna(x.median()))

# Filling missing values in 'model_year' and 'odometer' columns 
df['model_year'] = df.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))
df['odometer'] = df.groupby(['model', 'model_year'])['odometer'].transform(lambda x: x.fillna(x.median()))

# Strip extra spaces from column names
df.columns = df.columns.str.strip()


df = df[(df['model_year'] >= 1990) & (df['model_year'] <= 2025)]
df = df[(df['price'] > 100) & (df['price'] < 100000)]

df = df.dropna(subset=['price', 'odometer', 'model'])

# Sidebar filters
st.sidebar.header("Filter Listings")

# Dropdown: filter by model
models = df['model'].sort_values().unique()
selected_model = st.sidebar.selectbox("Choose a car model", options=models)

# Slider: filter by max price
max_price = int(df['price'].max())
selected_price = st.sidebar.slider("Maximum price", min_value=0, max_value=max_price, value=max_price)

# Checkbox: filter 4WD
only_4wd = st.sidebar.checkbox("Show only 4WD vehicles")

# Apply filters
filtered_df = df[df['model'] == selected_model]
filtered_df = filtered_df[filtered_df['price'] <= selected_price]
if only_4wd:
    filtered_df = filtered_df[filtered_df['is_4wd'] == 1.0]

# Show filtered data (optional for debugging)
# st.write(filtered_df.head())

# Dashboard title
st.header("Filtered Car Listings Dashboard")

# Histogram of prices
fig_price = px.histogram(filtered_df, x='price', title='Price Distribution')
st.plotly_chart(fig_price)

# Scatterplot of odometer vs price
if st.checkbox("Show Mileage vs Price"):
    fig_scatter = px.scatter(filtered_df, x='odometer', y='price', title='Mileage vs Price')
    st.plotly_chart(fig_scatter)
