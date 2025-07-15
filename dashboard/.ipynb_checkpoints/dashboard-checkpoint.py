# To run this: pip install streamlit, then in your terminal run: streamlit run dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Data (assuming the CSV is in the same folder) ---
@st.cache_data # Caches the data so it doesn't reload on every interaction
def load_data():
    df = pd.read_csv('../data/fitness_app_user_dataset.csv')
    return df

df = load_data()

# --- Build the Dashboard UI ---
st.title('Fitness App User Analysis Dashboard')
st.write("An interactive dashboard to explore user demographics and behavior.")

# --- Sidebar for Filters ---
st.sidebar.header('Filter Data')
selected_location = st.sidebar.multiselect(
    'Select Location(s)',
    options=df['Location'].unique(),
    default=df['Location'].unique()
)
selected_gender = st.sidebar.selectbox(
    'Select Gender',
    options=['All', 'Male', 'Female']
)

# --- Filter the dataframe based on selection ---
filtered_df = df[df['Location'].isin(selected_location)]
if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

# --- Main Page Layout ---
# KPI Cards
st.header('Key Performance Indicators')
col1, col2, col3 = st.columns(3)
col1.metric("Total Users", f"{filtered_df.shape[0]:,}")
col2.metric("Avg. Distance (km)", f"{filtered_df['Distance Travelled (km)'].mean():.1f}")
col3.metric("Avg. Calories Burned", f"{filtered_df['Calories Burned'].mean():.0f}")

st.markdown("---")

# Charts
st.header('Data Visualizations')
fig1 = px.histogram(
    filtered_df,
    x='Calories Burned',
    color='Activity Level',
    title='Distribution of Calories Burned by Activity Level'
)
st.plotly_chart(fig1)

fig2 = px.scatter(
    filtered_df,
    x='Distance Travelled (km)',
    y='Calories Burned',
    color='Gender',
    title='Distance vs. Calories by Gender'
)
st.plotly_chart(fig2)