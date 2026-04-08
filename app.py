import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="OptiCart Pro", layout="wide")

# 🔥 CUSTOM PROFESSIONAL CSS
st.markdown("""
<style>
body {
    background-color: #f4f6f8;
}
h1 {
    color: #2c3e50;
    font-weight: bold;
}
.card {
    padding: 15px;
    border-radius: 10px;
    background-color: white;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 10px;
}
.stButton>button {
    background-color: #2c3e50;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# 🔥 TITLE
st.title("OptiCart Pro – Smart Shopping Optimization System")

# 🔥 SIDEBAR
st.sidebar.header("Budget Settings")
budget = st.sidebar.number_input("Enter Budget (₹)", min_value=1)

num_products = st.sidebar.slider("Number of Products", 1, 8, 3)

st.subheader("Product Entry")

products = []

for i in range(num_products):
    st.markdown(f"### Product {i+1}")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        name = st.text_input("Name", key=f"name{i}")
    with col2:
        price = st.number_input("Price", key=f"price{i}")
    with col3:
        value = st.number_input("Rating/Value", key=f"value{i}")
    with col4:
        discount = st.slider("Discount %", 0, 50, key=f"disc{i}")

    final_price = price - (price * discount / 100)
    products.append((name, final_price, value, discount))

# 🔥 KNAPSACK
def knapsack(products, budget):
    n = len(products)
    dp = [[0]*(int(budget)+1) for _ in range(n+1)]

    for i in range(1, n+1):
        name, price, value, disc = products[i-1]
        for w in range(int(budget)+1):
            if price <= w:
                dp[i][w] = max(value + dp[i-1][int(w-price)], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    res = dp[n][int(budget)]

    w = int(budget)
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(products[i-1])
            w -= int(products[i-1][1])

    return res, selected

# 🔥 BUTTON
if st.button("Optimize Shopping"):

    max_value, selected = knapsack(products, budget)

    st.success(f"Maximum Value Achieved: {max_value}")

    df = pd.DataFrame(products, columns=["Product", "Final Price", "Value", "Discount"])

    # 🔥 METRICS
    total_cost = sum([p[1] for p in selected])
    total_items = len(selected)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Selected Items", total_items)
    with col2:
        st.metric("Total Cost", f"₹ {round(total_cost,2)}")

    # 🔥 TABLE
    st.subheader("All Products")
    st.dataframe(df)

    # 🔥 SELECTED PRODUCTS
    st.subheader("Recommended Products")

    for item in selected:
        st.markdown(f"""
        <div class="card">
        <b>{item[0]}</b><br>
        Price: ₹ {round(item[1],2)}<br>
        Discount: {item[3]}%
        </div>
        """, unsafe_allow_html=True)

    # 🔥 GRAPH
    st.subheader("Value Analysis")

    fig, ax = plt.subplots()
    ax.bar(df["Product"], df["Value"])
    ax.set_xlabel("Products")
    ax.set_ylabel("Value")
    st.pyplot(fig)

st.markdown("---")
st.markdown("OptiCart Pro | Advanced Budget Optimization System")
