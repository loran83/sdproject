import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('cleaned_vehicles_us.csv')
df.columns = df.columns.str.strip()
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
