import streamlit as st
import matplotlib.pyplot as plt

from db import get_customers
from data_preprocessing import final_df
from recommendation import recommend_products


st.sidebar.title(" Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Analytics"]
)


if page == "Home":

    st.title(" E-commerce Product Recommendation System")
    st.write("Welcome to the E-commerce Product Recommendation System!")

    
    customers = get_customers()

    
    selected_customer = st.selectbox(
        "Select Customer",
        customers["name"]
    )

    
    customer_id = customers.loc[
        customers["name"] == selected_customer,
        "customer_id"
    ].values[0]

    
    customer_info = customers[
        customers["customer_id"] == customer_id
    ]

    st.subheader(" Customer Details")

    st.write("**Name:**", customer_info["name"].values[0])
    st.write("**City:**", customer_info["city"].values[0])

    st.divider()

    
    purchased = final_df[
        final_df["customer_id"] == customer_id
    ]

    
    total_orders = purchased["order_id"].nunique()

    total_spending = (
        purchased["price"] * purchased["quantity"]
    ).sum()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Orders", total_orders)

    with col2:
        st.metric(" Total Spending", f"₹ {total_spending:,.2f}")

    st.divider()

    
    st.subheader("🛍 Purchased Products")

    st.dataframe(
        purchased[["product_name", "quantity", "price"]],
        use_container_width=True
    )

    st.divider()

    
    st.subheader("Recommended Products")

    recommendations = recommend_products(customer_id)

    recommendations["predicted_rating"] = (
        recommendations["predicted_rating"].round(2)
    )

    st.dataframe(
        recommendations[
            ["product_name", "price", "predicted_rating"]
        ],
        use_container_width=True
    )
elif page == "Analytics":

    st.title("📊 Analytics Dashboard")

    
    st.subheader(" Top Selling Products")

    top_products = (
        final_df.groupby("product_name")["quantity"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    colors = ["#4CAF50", "#2196F3", "#FFC107", "#FF5722", "#9C27B0"]

    ax.bar(
        top_products.index,
        top_products.values,
        color=colors,
        edgecolor="black"
    )

    for i, value in enumerate(top_products.values):
        ax.text(
            i,
            value + 0.1,
            str(value),
            ha="center",
            fontsize=10,
            fontweight="bold"
        )

    ax.set_title("Top Selling Products")
    ax.set_xlabel("Product Name")
    ax.set_ylabel("Quantity Sold")

    plt.xticks(rotation=45)

    st.pyplot(fig)

    st.divider()

    
    st.subheader(" Revenue by Product")

    revenue_df = final_df.copy()

    revenue_df["Revenue"] = (
        revenue_df["price"] * revenue_df["quantity"]
    )

    product_revenue = (
        revenue_df.groupby("product_name")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 4))

    colors = ["#FF6F61", "#6A5ACD", "#20B2AA", "#FFA500", "#3CB371"]

    ax.bar(
        product_revenue.index,
        product_revenue.values,
        color=colors,
        edgecolor="black"
    )

    for i, value in enumerate(product_revenue.values):
        ax.text(
            i,
            value + 1000,
            f"₹{int(value)}",
            ha="center",
            fontsize=9,
            fontweight="bold"
        )

    ax.set_title("Revenue by Product")
    ax.set_xlabel("Product Name")
    ax.set_ylabel("Revenue (₹)")

    plt.xticks(rotation=45)

    st.pyplot(fig)

    st.divider()

   
    st.subheader(" Product Sales Distribution")

    sales = (
        final_df.groupby("product_name")["quantity"]
        .sum()
    )

    fig, ax = plt.subplots(figsize=(6, 6))

    colors = [
        "#4CAF50",
        "#2196F3",
        "#FFC107",
        "#FF5722",
        "#9C27B0"
    ]

    ax.pie(
        sales.values,
        labels=sales.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors,
        explode=[0.05] * len(sales)
    )

    ax.set_title("Product Sales Distribution")

    st.pyplot(fig)

