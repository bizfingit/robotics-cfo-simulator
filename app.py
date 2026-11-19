import streamlit as st
import pandas as pd

st.set_page_config(page_title="BizFin | RoboScale CFO Portal", page_icon="🤖", layout="wide")

# Header
st.title("🤖 RoboScale CFO — Financial Engineering Portal")
st.markdown("**By BizFin** | Extending Runway & Unlocking Working Capital for US Robotics & Hardware Startups.")

# Sidebar Inputs
st.sidebar.header("⚙️ 1. Company Baseline")
starting_cash = st.sidebar.number_input("Starting Cash in Bank ($)", min_value=100000, max_value=20000000, value=2000000, step=100000)
bom_cost = st.sidebar.slider("Current Unit Cost / BOM ($)", min_value=1000, max_value=25000, value=6870, step=100)
selling_price = st.sidebar.slider("Selling Price per Robot ($)", min_value=5000, max_value=50000, value=15000, step=500)
monthly_opex = st.sidebar.number_input("Fixed Monthly OpEx ($)", min_value=10000, max_value=1000000, value=100000, step=5000)
lead_time_months = st.sidebar.slider("Supplier Lead Time (Months Advance)", min_value=0, max_value=3, value=2)

st.sidebar.divider()
st.sidebar.header("🚀 2. BizFin CFO Levers (Solutions)")
bom_reduction_pct = st.sidebar.slider("BOM Cost Optimization (%)", min_value=0, max_value=30, value=15, step=1)
customer_deposit_pct = st.sidebar.slider("Customer Upfront Deposit (%)", min_value=0, max_value=50, value=30, step=5)

# Core Calculations
optimized_bom = bom_cost * (1 - bom_reduction_pct / 100)
gross_profit = selling_price - bom_cost
gross_margin = (gross_profit / selling_price) * 100 if selling_price > 0 else 0
opt_gross_margin = ((selling_price - optimized_bom) / selling_price) * 100 if selling_price > 0 else 0
breakeven_units = (monthly_opex / gross_profit) if gross_profit > 0 else 0

sales_schedule = [2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20]
extended_sales = sales_schedule + [22, 24, 26]

rows = []
forecast_cash = starting_cash
real_cash = starting_cash
cfo_optimized_cash = starting_cash

for i in range(12):
    month = f"Month {i+1:02d}"
    units = sales_schedule[i]
    rev = units * selling_price
    
    # 1. Paper Forecast
    cogs_standard = units * bom_cost
    forecast_cash += (rev - cogs_standard - monthly_opex)
    
    # 2. Real Cash (Status Quo - No CFO)
    advance_units = extended_sales[i + lead_time_months]
    cogs_real = advance_units * bom_cost
    real_cash += (rev - cogs_real - monthly_opex)
    
    # 3. With BizFin CFO (Optimized BOM + Customer Deposits)
    deposit_inflow = (advance_units * selling_price) * (customer_deposit_pct / 100)
    remaining_rev = rev * (1 - customer_deposit_pct / 100)
    cogs_opt = advance_units * optimized_bom
    cfo_optimized_cash += (remaining_rev + deposit_inflow - cogs_opt - monthly_opex)
    
    rows.append({
        "Month": month,
        "Robots Sold": units,
        "Revenue ($)": rev,
        "Paper Forecast Cash ($)": round(forecast_cash),
        "Status Quo Real Cash ($)": round(real_cash),
        "With BizFin CFO Cash ($)": round(cfo_optimized_cash),
        "Cash Trapped ($)": round(real_cash - forecast_cash),
        "Extra Cash Unlocked by CFO ($)": round(cfo_optimized_cash - real_cash)
    })

df = pd.DataFrame(rows)
cash_unlocked = df["Extra Cash Unlocked by CFO ($)"].iloc[-1]

# Multi-Tab Navigation
tab1, tab2, tab3 = st.tabs([
    "📊 1. Runway & Working Capital Simulator", 
    "⚙️ 2. BOM & Margin Optimizer", 
    "🗺️ 3. A-to-Z Deliverables (What You Get)"
])

# --- TAB 1: RUNWAY & WORKING CAPITAL ---
with tab1:
    st.subheader("Executive Snapshot: Status Quo vs. BizFin Optimization")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current Gross Margin", f"{gross_margin:.1f}%", f"+{opt_gross_margin - gross_margin:.1f}% Optimized")
    c2.metric("Break-Even Volume", f"{breakeven_units:.1f} robots/mo" if gross_profit > 0 else "N/A")
    c3.metric("Cash Trapped (Month 12)", f"${df['Cash Trapped ($)'].iloc[-1]:,.0f}", delta_color="inverse")
    c4.metric("Extra Cash Unlocked (CFO)", f"+${cash_unlocked:,.0f}", "Via BOM + Deposits")

    st.divider()
    st.subheader("📈 Cash Trajectory: Paper Forecast vs. Reality vs. BizFin CFO")
    chart_data = df.set_index("Month")[[
        "Paper Forecast Cash ($)", 
        "Status Quo Real Cash ($)", 
        "With BizFin CFO Cash ($)"
    ]]
    st.line_chart(chart_data)
    
    st.info(f"💡 **CFO Insight:** Without working capital engineering, your {lead_time_months}-month supplier lead time traps **${abs(df['Cash Trapped ($)'].iloc[-1]):,.0f}**. By applying a **{bom_reduction_pct}% BOM optimization** and **{customer_deposit_pct}% upfront customer deposits**, BizFin unlocks **${cash_unlocked:,.0f}** in additional bank cash by Month 12 — without diluting equity.")

    st.subheader("📋 12-Month Detailed Cash Flow Table")
    st.dataframe(df, use_container_width=True)
    
    # Download CSV Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Custom 12-Month Financial Model (CSV)",
        data=csv,
        file_name="BizFin_Robotics_CFO_Forecast.csv",
        mime="text/csv"
    )

# --- TAB 2: BOM OPTIMIZER ---
with tab2:
    st.subheader("Unit Economics & Supply Chain Impact")
    total_units = sum(sales_schedule)
    annual_bom_savings = (bom_cost - optimized_bom) * total_units
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Current BOM / Unit", f"${bom_cost:,.0f}")
    col_b.metric("Target Optimized BOM", f"${optimized_bom:,.0f}", f"-{bom_reduction_pct}%")
    col_c.metric("Year 1 Pure Profit Added", f"+${annual_bom_savings:,.0f}", f"Across {total_units} robots")
    
    st.markdown("""
    ### How We Achieve 10%–20% BOM Reduction:
    * **Component Consolidation:** Identifying overpriced Actuators, LiDAR, and Battery suppliers.
    * **Payment Term Restructuring:** Shifting suppliers from 100% upfront to Net-30 / Net-60 terms.
    * **Assembly Labor Efficiency:** Tracking per-unit labor hours to eliminate factory floor bottlenecks.
    """)

# --- TAB 3: A-TO-Z DELIVERABLES ---
with tab3:
    st.subheader("What You Get with RoboScale CFO (A-to-Z Roadmap)")
    st.markdown("We don't just send spreadsheets. We operate as your **Asynchronous Financial Engineering Desk**.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🔹 Days 1–30: Foundation & Audit")
        st.markdown("""
        - Complete **BOM & Unit Economics Audit**
        - Supplier Lead Time & **Working Capital Trap** mapping
        - Clean separation of R&D Burn vs. Manufacturing COGS
        - Automated connection to QuickBooks / Xero / ERP
        """)
    with col2:
        st.markdown("### 🔹 Days 31–60: Live Automation")
        st.markdown("""
        - 24/7 **Live Executive Cash Runway Dashboard**
        - Automated Weekly Burn & Cash Trough alerts
        - **What-If Scenario Modeling** (Hiring, Factory Scaling)
        - Customer Deposit & Supplier Net-60 negotiation playbooks
        """)
    with col3:
        st.markdown("### 🔹 Days 61–90: Scale & Capital")
        st.markdown("""
        - **Investor-Ready Board Decks** & Series A Data Room
        - **Non-Dilutive Venture Debt** & Equipment Financing models
        - R&D Tax Credit optimization strategy
        - Ongoing monthly Fractional CFO advisory
        """)
        
    st.divider()
    st.success("🎯 **Ready to unlock your trapped working capital?**")
    st.markdown("Reply to our email or connect on LinkedIn to get a **Free Custom 12-Month Working Capital Audit** built with your startup's actual numbers.")
