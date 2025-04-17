# Zomato Live Sales Dashboard

This project showcases a **Zomato Live Sales Dashboard** built using **Streamlit**, **Pandas**, **Altair**, **Seaborn**, and **Matplotlib** to visualize and analyze live sales data from food delivery apps.

## Features:
- Real-time sales data metrics
- Sales trend over time
- Top-selling items
- City-specific item sales with horizontal bar plots
- Sales prediction using machine learning (Prophet)
- Interactive maps with Folium

## Tech Stack:
- **Streamlit** for dashboard UI
- **Pandas**, **Altair**, **Seaborn**, and **Matplotlib** for data visualization
- **Prophet** for forecasting
- **Folium** for interactive maps

## How to Run:
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/zomato-sales-dashboard.git
   pip install -r requirements.txt
   streamlit run zomato_dashboard.py


### Step 5: **Data (sales.csv)**

If you don't have the actual `sales.csv`, create a mock file with the following example data structure:

```csv
timestamp,city,item,price,quantity
2025-04-01 00:00:00,Delhi,Burger,150,10
2025-04-01 00:05:00,Delhi,Pizza,200,15
2025-04-01 00:10:00,Bangalore,Pasta,120,8
2025-04-01 00:15:00,Mumbai,Burger,150,20


