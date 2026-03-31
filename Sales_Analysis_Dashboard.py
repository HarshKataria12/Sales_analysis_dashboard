import pandas as pd
import sqlite3
import kagglehub
import os
import dash
from dash import html, dcc, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go


# Download dataset
path = kagglehub.dataset_download("vivek468/superstore-dataset-final")

# Find the CSV file inside the downloaded folder
files = os.listdir(path)
csv_file = [f for f in files if f.endswith('.csv')][0]
csv_path = os.path.join(path, csv_file)

# Load CSV into DataFrame
df = pd.read_csv(csv_path, encoding='latin-1')
print(df.columns.tolist())

# Connect to SQLite database
conn = sqlite3.connect('sales_data.db')

# Save DataFrame to SQLite table
df.to_sql('sales', conn, if_exists='replace', index=False)

# Query data from SQLite

# Total Sales From Region
query_region_sales = """
Select Region, sum(Sales) as Total_Sales 
From sales
Group by Region
"""
# Top 10 Products by Revenue
query_top_products = """
SELECT "Product Name", SUM(Sales) AS Revenue
FROM sales
GROUP BY "Product Name"
ORDER BY Revenue DESC
LIMIT 10
"""
# Monthly Sales Trend
query_monthly_sales = """
SELECT 
  substr("Order Date", -4) || '-' || 
  printf('%02d', substr("Order Date", 1, instr("Order Date", '/') - 1))
AS Month,
  SUM(Sales) AS Total_Sales
FROM sales  
GROUP BY Month
ORDER BY Month
LIMIT 5;
"""
# Profit margin by category
# Profit Margin = Total Profit ÷ Total Sales
# reason for multiplying by 1.0 is to ensure that the division results in a float, giving us a more accurate profit margin percentage.
query_profit_margin = """
SELECT Category,
       SUM(Profit) * 1.0 / SUM(Sales) AS Profit_Margin
FROM sales
GROUP BY Category
"""

# States with highest and lowest sales
query_states = """
SELECT State, SUM(Sales) AS Total_Sales
FROM sales
GROUP BY State
ORDER BY Total_Sales DESC
"""
# load the result into a DataFrame
df_region_sales = pd.read_sql_query(query_region_sales, conn).round(2)
df_top_products = pd.read_sql_query(query_top_products, conn).round(2)
df_monthly_sales = pd.read_sql_query(query_monthly_sales, conn).round(2)
df_profit_margin = pd.read_sql_query(query_profit_margin, conn).round(2)
df_states = pd.read_sql_query(query_states, conn).round(2)

# Close connection
conn.close()
# print(df_region_sales)
# print(df_top_products)
print(df_monthly_sales)
# print(df_profit_margin)
# print(df_states)

# ── Create figures from DataFrames ───────────
 
fig1 = px.pie(df_region_sales, names="Region", values="Total_Sales", title="Sales by Region")
 
fig2 = px.bar(df_top_products, x="Revenue", y="Product Name", orientation="h", title="Top 10 Products by Revenue")
 
fig3 = px.line(df_monthly_sales, x="Month", y="Total_Sales", title="Monthly Sales Trend")
 
fig4 = px.bar(df_profit_margin, x="Category", y="Profit_Margin", title="Profit Margin by Category")
 
fig5 = px.bar(df_states.head(10), x="Total_Sales", y="State", orientation="h", title="Top 10 States by Sales")
 
# ── Create Dash App ───────────
# ── Dash App ─────────────────────────────────
 
app = dash.Dash(__name__)
 
app.layout = html.Div(children=[
 
    html.H1("Supermarket Sales Dashboard"),
 
    dcc.Graph(figure=fig1),
 
    dcc.Graph(figure=fig2),
 
    dcc.Graph(figure=fig3),
 
    dcc.Graph(figure=fig4),
 
    dcc.Graph(figure=fig5),
 
])
 
if __name__ == "__main__":
    app.run(debug=True)
 

