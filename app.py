import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Amazon Smart Optimizer", layout="wide")

# 🔥 Custom CSS (Amazon style)
st.markdown("""
<style>
body {
    background-color: #f5f5f5;
}
.main {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 10px;
}
h1 {
    color: #ff9900;
}
.stButton>button {
    background-color: #ff9900;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("🛒 Amazon Smart Shopping Optimizer")

# Sidebar
st.sidebar.header("💰 Budget Settings")
budget = st.sidebar.number_input("Enter Budget ₹", min_value=1)

num_products = st.sidebar.slider("Number of Products", 1, 8, 3)

st.subheader("📦 Add Products")

products = []

for i in range(num_products):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name = st.text_input(f"Product {i+1}", key=f"name{i}")
    with col2:
        price = st.number_input(f"Price ₹{i+1}", key=f"price{i}")
    with col3:
        value = st.number_input(f"Rating/Value {i+1}", key=f"value{i}")
    
    products.append((name, price, value))

def knapsack(products, budget):
    n = len(products)
    dp = [[0]*(int(budget)+1) for _ in range(n+1)]

    for i in range(1, n+1):
        name, price, value = products[i-1]
        for w in range(int(budget)+1):
            if price <= w:
                dp[i][w] = max(value + dp[i-1][w-int(price)], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    res = dp[n][int(budget)]

    w = int(budget)
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(products[i-1][0])
            w -= int(products[i-1][1])

    return res, selected

if st.button("🚀 Optimize Shopping"):
    max_value, selected = knapsack(products, budget)

    st.success(f"💎 Maximum Value Achieved: {max_value}")

    df = pd.DataFrame(products, columns=["Product", "Price", "Value"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Product Table")
        st.dataframe(df)

    with col2:
        st.subheader("🛍️ Recommended Products")
        for item in selected:
            st.markdown(f"🟢 **{item}**")

    st.subheader("📈 Analysis Graph")

    fig, ax = plt.subplots()
    ax.bar(df["Product"], df["Value"])
    st.pyplot(fig)

st.markdown("---")
st.markdown("✨ AI-Powered Shopping Optimization System")
