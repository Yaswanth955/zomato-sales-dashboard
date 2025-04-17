import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from prophet import Prophet
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import seaborn as sns

st.set_page_config(page_title="Zomato Live Sales Dashboard", layout="wide")
st.title("🍽️ Zomato Live Sales Dashboard")

# Load data
@st.cache_data(ttl=30)
def load_data():
    df = pd.read_csv('sales.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

df = load_data()

# Date filter
st.subheader("📅 Filter by Date Range")
min_date = df['timestamp'].min().date()
max_date = df['timestamp'].max().date()
start_date, end_date = st.date_input("Select Date Range", [min_date, max_date])
df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

# Metrics
st.subheader("📌 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"₹{df['price'].sum():,.0f}")
col2.metric("Total Orders", f"{len(df)}")
col3.metric("Top City", df['city'].value_counts().idxmax())

# Sales Over Time
st.subheader("📈 Sales Over Time by City")
df['minute'] = df['timestamp'].dt.strftime('%H:%M')
sales_chart = alt.Chart(df).mark_line().encode(
    x='minute',
    y='price',
    color='city'
).properties(width=800, height=400)
st.altair_chart(sales_chart, use_container_width=True)

# City-wise Small Plots
st.subheader("🌆 City-wise Sales Overview")
cities = df['city'].unique()
city_cols = st.columns(len(cities))
for i, city in enumerate(cities):
    with city_cols[i]:
        st.markdown(f"**{city}**")
        city_data = df[df['city'] == city].groupby('minute')['price'].sum()
        st.line_chart(city_data)

# Word Cloud of Items
st.subheader("🍕 Word Cloud of Sold Items")
text = " ".join(df['item'])
wc = WordCloud(width=800, height=400, background_color='white', colormap='plasma').generate(text)
fig_wc, ax_wc = plt.subplots()
ax_wc.imshow(wc, interpolation='bilinear')
ax_wc.axis('off')
st.pyplot(fig_wc)

# Forecasting with Prophet
st.subheader("🔮 Sales Forecast (Next 24 Hours)")
forecast_df = df.groupby(df['timestamp'].dt.floor('H'))['price'].sum().reset_index()
forecast_df.columns = ['ds', 'y']
if len(forecast_df) > 1:
    model = Prophet()
    model.fit(forecast_df)
    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)
    fig1 = model.plot(forecast)
    st.pyplot(fig1)
else:
    st.warning("📉 Not enough data for forecasting. Try selecting a larger date range.")

# Interactive Map
st.subheader("🗺️ Sales Map by City")
city_sales = df.groupby('city')['price'].sum().reset_index()

# Dummy city coordinates (you can replace with real lat/long if available)
city_coords = {
    "Mumbai": [19.0760, 72.8777],
    "Delhi": [28.7041, 77.1025],
    "Bangalore": [12.9716, 77.5946],
    "Hyderabad": [17.3850, 78.4867],
    "Chennai": [13.0827, 80.2707],
}

m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
for _, row in city_sales.iterrows():
    city = row['city']
    sales = row['price']
    lat, lon = city_coords.get(city, [20.5937, 78.9629])
    folium.Circle(
        location=[lat, lon],
        radius=10,
        popup=f"{city}: ₹{sales:,.0f}",
        color="crimson",
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

folium_static(m, width=700, height=400)

st.caption("🔄 Auto-refresh every 30s using caching. Run data simulator in background.")

# Top-Selling Items
st.subheader("🔥 Top-Selling Items")
top_items = df.groupby('item')['quantity'].sum().sort_values(ascending=False)
st.bar_chart(top_items)

# Item Sales in Each City - Horizontal Bar Plot
st.subheader("📊 Item Sales in Each City")
# Group by city and item and sum up the quantities sold
city_item_sales = df.groupby(['city', 'item'])['quantity'].sum().reset_index()

# Use Seaborn to create a horizontal bar plot with different colors for each city
plt.figure(figsize=(10, 6))
sns.set_palette("tab10")  # Set a color palette
city_sales_plot = sns.barplot(data=city_item_sales, y='item', x='quantity', hue='city', dodge=True)
city_sales_plot.set_xlabel('Quantity Sold')
city_sales_plot.set_ylabel('Item')
city_sales_plot.set_title('Item Sales in Each City')

# Display the plot in Streamlit
st.pyplot(plt)

# Footer
st.caption("⏱️ Auto-refresh every 30s using caching. Run data simulator in background.")
