# ================================
# ADVANCED STOCK PORTFOLIO DASHBOARD
# ================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ================================
# PAGE CONFIG
# ================================

st.set_page_config(
    page_title="Advanced Stock Portfolio",
    page_icon="📈",
    layout="wide"
)

# ================================
# CUSTOM CSS
# ================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

h1,h2,h3 {
    color: #4CAF50;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

.stDownloadButton>button {
    background-color: #2196F3;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}

div[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border: 1px solid #4CAF50;
    padding: 15px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ================================
# CSV FILE SETUP
# ================================

FILE_NAME = "portfolio_data.csv"

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "Stock",
        "Quantity",
        "Buy Price",
        "Sell Price",
        "Investment",
        "Profit",
        "Profit %"
    ])
    df.to_csv(FILE_NAME, index=False)

df = pd.read_csv(FILE_NAME)

# ================================
# SIDEBAR
# ================================

st.sidebar.title("📊 Portfolio Dashboard")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Add Stock",
        "Portfolio Overview",
        "Edit Stock",
        "Delete Stock"
    ]
)

# ================================
# TITLE
# ================================

st.title("📈 Advanced Stock Portfolio Dashboard")

# ================================
# ADD STOCK SECTION
# ================================

if menu == "Add Stock":

    st.header("➕ Add New Stock")

    col1, col2 = st.columns(2)

    with col1:
        stock_name = st.text_input("Stock Name")

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1
        )

    with col2:
        buy_price = st.number_input(
            "Buy Price",
            min_value=0.0
        )

        sell_price = st.number_input(
            "Sell Price",
            min_value=0.0
        )

    if st.button("Add Stock"):

        investment = quantity * buy_price

        profit = (sell_price - buy_price) * quantity

        profit_percent = (
            (profit / investment) * 100
            if investment != 0 else 0
        )

        new_data = pd.DataFrame({
            "Stock": [stock_name],
            "Quantity": [quantity],
            "Buy Price": [buy_price],
            "Sell Price": [sell_price],
            "Investment": [investment],
            "Profit": [profit],
            "Profit %": [profit_percent]
        })

        df = pd.concat([df, new_data], ignore_index=True)

        # AUTO SAVE
        df.to_csv(FILE_NAME, index=False)

        st.success("✅ Stock Added & Auto Saved Successfully")

# ================================
# PORTFOLIO OVERVIEW
# ================================

elif menu == "Portfolio Overview":

    st.header("📋 Portfolio Overview")

    if len(df) == 0:
        st.warning("No Stocks Added Yet")

    else:

        # ================================
        # TABLE
        # ================================

        st.subheader("📊 Stock Performance Table")

        st.dataframe(
            df,
            use_container_width=True
        )

        # ================================
        # SUMMARY METRICS
        # ================================

        total_investment = df["Investment"].sum()

        total_profit = df["Profit"].sum()

        total_profit_percent = (
            (total_profit / total_investment) * 100
            if total_investment != 0 else 0
        )

        st.subheader("📌 Portfolio Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💰 Total Investment",
                f"₹ {total_investment:,.2f}"
            )

        with col2:
            st.metric(
                "📈 Total Profit",
                f"₹ {total_profit:,.2f}"
            )

        with col3:
            st.metric(
                "🚀 Profit Percentage",
                f"{total_profit_percent:.2f}%"
            )

        # ================================
        # BAR GRAPH
        # ================================

        st.subheader("📊 Best Performing Stocks")

        fig = px.bar(
            df,
            x="Stock",
            y="Profit %",
            text="Profit %",
            title="Stock Profit Percentage"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ================================
        # INDIVIDUAL STOCK PIE CHART
        # ================================

        st.subheader("🥧 Individual Stock Performance")

        selected_stock = st.selectbox(
            "Select Stock",
            df["Stock"]
        )

        stock_data = df[df["Stock"] == selected_stock]

        pie_df = pd.DataFrame({
            "Category": ["Investment", "Profit"],
            "Value": [
                stock_data["Investment"].values[0],
                stock_data["Profit"].values[0]
            ]
        })

        pie_fig = px.pie(
            pie_df,
            names="Category",
            values="Value",
            title=f"{selected_stock} Performance"
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )

        # ================================
        # OVERALL PIE CHART
        # ================================

        st.subheader("🥧 Overall Portfolio Profit Distribution")

        overall_pie = px.pie(
            df,
            names="Stock",
            values="Profit",
            title="Profit Contribution Of Each Stock"
        )

        st.plotly_chart(
            overall_pie,
            use_container_width=True
        )

        # ================================
        # DOWNLOAD CSV
        # ================================

        st.subheader("⬇ Download Portfolio")

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Portfolio CSV",
            data=csv,
            file_name="portfolio_data.csv",
            mime="text/csv"
        )

# ================================
# EDIT STOCK
# ================================

elif menu == "Edit Stock":

    st.header("✏ Edit Stock")

    if len(df) == 0:
        st.warning("No Stocks Available")

    else:

        edit_stock = st.selectbox(
            "Select Stock To Edit",
            df["Stock"].unique()
        )

        selected_row = df[df["Stock"] == edit_stock].iloc[0]

        new_quantity = st.number_input(
            "New Quantity",
            value=int(selected_row["Quantity"])
        )

        new_buy_price = st.number_input(
            "New Buy Price",
            value=float(selected_row["Buy Price"])
        )

        new_sell_price = st.number_input(
            "New Sell Price",
            value=float(selected_row["Sell Price"])
        )

        if st.button("Update Stock"):

            investment = new_quantity * new_buy_price

            profit = (
                (new_sell_price - new_buy_price)
                * new_quantity
            )

            profit_percent = (
                (profit / investment) * 100
                if investment != 0 else 0
            )

            df.loc[
                df["Stock"] == edit_stock,
                "Quantity"
            ] = new_quantity

            df.loc[
                df["Stock"] == edit_stock,
                "Buy Price"
            ] = new_buy_price

            df.loc[
                df["Stock"] == edit_stock,
                "Sell Price"
            ] = new_sell_price

            df.loc[
                df["Stock"] == edit_stock,
                "Investment"
            ] = investment

            df.loc[
                df["Stock"] == edit_stock,
                "Profit"
            ] = profit

            df.loc[
                df["Stock"] == edit_stock,
                "Profit %"
            ] = profit_percent

            df.to_csv(FILE_NAME, index=False)

            st.success("✅ Stock Updated Successfully")

# ================================
# DELETE STOCK
# ================================

elif menu == "Delete Stock":

    st.header("🗑 Delete Stock")

    if len(df) == 0:
        st.warning("No Stocks Available")

    else:

        delete_stock = st.selectbox(
            "Select Stock To Delete",
            df["Stock"].unique()
        )

        if st.button("Delete Stock"):

            df = df[df["Stock"] != delete_stock]

            df.to_csv(FILE_NAME, index=False)

            st.success(
                f"✅ {delete_stock} Deleted Successfully"
            )
            