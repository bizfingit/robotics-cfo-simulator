import streamlit as st
import pandas as pd

st.set_page_config(page_title="BizFin | Robotics CFO Simulator", layout="wide")

st.title("🤖 Robotics Cash Runway & Working Capital Simulator")
st.markdown("Built by **BizFin** — Interactive Financial Engineering for US Hardware & Robotics Startups.")

# Sidebar Inputs (Sliders)
st.sidebar.header("⚙️ Company Assumptions")
starting_cash = st.sidebar.number_input("Starting Cash in Bank ($)", min_value=100000, max_value=20000000, value=2000000, step=100000)
bom_cost = st.sidebar.slider("Unit Cost / BOM ($)", min_value=1000, max_value=25000, value=6870, step=100)
selling_price = st.sidebar.slider("Selling Price per Robot ($)", min_value=5000, max_value=50000, value=15000, step=500)
monthly_opex = st.sidebar.number_input("Fixed Monthly OpEx ($)", min_value=10000, max_value=1000000, value=100000, step=5000)
lead_time_months = st.sidebar.slider("Supplier Lead Time (Months Advance)", min_value=0, max_value=3, value=2)

# Unit Economics Calculations
gross_profit = selling_price - bom_cost
gross_margin = (gross_profit / selling_price) * 100 if selling_price > 0 else 0
breakeven_units = (monthly_opex / gross_profit) if gross_profit > 0 else 0

# 12-Month Sales Schedule (Base Growth)
sales_schedule = [2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20]
extended_sales = sales_schedule + [22, 24, 26] # For advance BOM calculation

rows = []
forecast_cash = starting_cash
real_cash = starting_cash

for i in range(12):
    month = f"Month {i+1:02d}"
    units = sales_schedule[i]
    rev = units * selling_price
    
    # Standard Forecast (Same-month BOM)
    cogs_standard = units * bom_cost
    net_cf_standard = rev - cogs_standard - monthly_opex
    forecast_cash += net_cf_standard
    
    # Real Working Capital (Advance BOM based on Lead Time)
    advance_units = extended_sales[i + lead_time_months]
    cogs_real = advance_units * bom_cost
    net_cf_real = rev - cogs_real - monthly_opex
    real_cash += net_cf_real
    
    rows.append({
        "Month": month,
        "Robots Sold": units,
        "Revenue ($)": rev,
        "Forecast Cash ($)": forecast_cash,
        "Real Cash - After Lead Time ($)": real_cash,
        "Cash Trapped ($)": real_cash - forecast_cash
    })

df = pd.DataFrame(rows)

# Top KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Gross Margin", f"{gross_margin:.1f}%")
col2.metric("Break-Even Volume", f"{breakeven_units:.1f} robots/mo" if gross_profit > 0 else "N/A")
col3.metric("Lowest Real Cash (Trough)", f"${df['Real Cash - After Lead Time ($)'].min():,.0f}")
col4.metric("Cash Trapped (Month 12)", f"${df['Cash Trapped ($)'].iloc[-1]:,.0f}")

st.divider()

# Interactive Chart
st.subheader("📈 Cash Runway: Paper Forecast vs. Real Working Capital")
chart_data = df.set_index("Month")[["Forecast Cash ($)", "Real Cash - After Lead Time ($)"]]
st.line_chart(chart_data)

# Data Table
st.subheader("📊 12-Month Financial Breakdown")
st.dataframe(df, use_container_width=True)
