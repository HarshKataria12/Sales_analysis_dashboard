# Supermarket Sales Dashboard

Interactive sales dashboard built with Python. Takes raw CSV data through a pipeline: **CSV → SQLite → Pandas → Dash**.

## Data Pipeline

1. Download dataset from Kaggle
2. Load CSV into Pandas DataFrame
3. Store in SQLite database
4. Query data using SQL
5. Visualize with Plotly charts in a Dash web app

## Charts

- Sales by Region (pie chart)
- Top 10 Products by Revenue (bar chart)
- Monthly Sales Trend (line chart)
- Profit Margin by Category (bar chart)
- Top 10 States by Sales (bar chart)

## Tech Stack

Python, Pandas, SQLite, Plotly, Dash, KaggleHub

## Setup

```bash
git clone https://github.com/yourusername/Sales_analysis_dashboard.git
cd Sales_analysis_dashboard
pip install -r requirements.txt
python Sales_Analysis_Dashboard.py
```

Open http://127.0.0.1:8050 in your browser.

## Dataset

[Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) from Kaggle — 9,994 rows, 21 columns, zero missing values.# Sales_analysis_dashboard
