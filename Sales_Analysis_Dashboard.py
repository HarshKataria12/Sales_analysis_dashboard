import pandas as pd
import sqlite3
import kagglehub
import os

# Download dataset
path = kagglehub.dataset_download("bravehart101/sample-supermarket-dataset")

# Find the CSV file inside the downloaded folder
files = os.listdir(path)
csv_file = [f for f in files if f.endswith('.csv')][0]
csv_path = os.path.join(path, csv_file)

# Load CSV into DataFrame
df = pd.read_csv(csv_path)

# Connect to SQLite database
conn = sqlite3.connect('sales_data.db')

# Save DataFrame to SQLite table
df.to_sql('sales', conn, if_exists='replace', index=False)

# Query data from SQLite

# Total Sales From Region
query_region_sales = """
Select Region, sum(Total_Sales) as Total_Sales 
From sales
Group by Region
"""
# Top 10 Products by Revenue
query_top_products = """
SELECT Product_Name, SUM(Sales) AS Revenue
FROM sales
GROUP BY Product_Name
ORDER BY Revenue DESC
LIMIT 10
"""
# Monthly Sales Trend
query_monthly_sales = """
SELECT strftime('%Y-%m', "Order Date") AS Month, SUM(Sales) AS Total_Sales
FROM sales  
GROUP BY Month
ORDER BY Month
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
df_region_sales = pd.read_sql_query(query_region_sales, conn)
df_top_products = pd.read_sql_query(query_top_products, conn)
df_monthly_sales = pd.read_sql_query(query_monthly_sales, conn)
df_profit_margin = pd.read_sql_query(query_profit_margin, conn)
df_states = pd.read_sql_query(query_states, conn)


# Close connection
conn.close()

print(df.head())