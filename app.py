import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="OptiCart Pro", layout="wide")

# 🎨 MODERN UI
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #eef2ff, #ffffff);
}
h1 {
    color: #1a237e;
    text-align: center;
}
.card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
.stButton>button {
    background: linear-gradient(to right, #1a237e, #3949ab);
    color: white;
    height: 50px;
    border-radius: 10px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# 🏷️ TITLE
st.title("OptiCart Pro – Smart Shopping Optimization System")

# 📊 SIDEBAR
st.sidebar.header("Budget Settings")
budget = st.sidebar.number_input("Enter Budget (₹)", min_value=1)

num_products = st.sidebar.slider("Number of Products", 1, 10, 3)

# 🧭 TABS
tab1, tab2, tab3 = st.tabs(["Product Entry", "Results", "Analysis"])

products = []

# ------------------- TAB 1 -------------------
with tab1:
    st.subheader("Enter Product Details")

    for i in range(num_products):
        st.markdown(f"<div class='card'>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            name = st.text_input(f"Product {i+1} Name", key=f"name{i}")
        with col2:
            price = st.number_input(f"Price ₹{i+1}", key=f"price{i}")
        with col3:
            value = st.number_input(f"Rating {i+1}", key=f"value{i}")
        with col4:
            discount = st.slider(f"Discount {i+1} %", 0, 50, key=f"disc{i}")

        final_price = price - (price * discount / 100)

        st.markdown(f"Final Price: ₹ {round(final_price,2)}")

        st.markdown("</div>", unsafe_allow_html=True)

        products.append((name, final_price, value))

# 🧠 KNAPSACK FUNCTION
def knapsack(products, budget):
    n = len(products)
    dp = [[0]*(int(budget)+1) for _ in range(n+1)]

    for i in range(1, n+1):
        name, price, value = products[i-1]
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

# 🔘 BUTTON
run = st.button("Optimize Shopping")

# ------------------- TAB 2 -------------------
with tab2:
    if run:
        max_value, selected = knapsack(products, budget)

        st.success(f"Maximum Value Achieved: {max_value}")

        total_cost = sum([p[1] for p in selected])

        col1, col2 = st.columns(2)
        col1.metric("Total Items Selected", len(selected))
        col2.metric("Total Cost", f"₹ {round(total_cost,2)}")

        st.subheader("Recommended Products")

        for item in selected:
            st.markdown(f"""
            <div class='card'>
            <b>{item[0]}</b><br>
            Price: ₹ {round(item[1],2)}
            </div>
            """, unsafe_allow_html=True)

        df = pd.DataFrame(products, columns=["Product", "Price", "Value"])

        st.subheader("All Products")
        st.dataframe(df)

# ------------------- TAB 3 -------------------
with tab3:
    if run:
        df = pd.DataFrame(products, columns=["Product", "Price", "Value"])

        st.subheader("Price vs Value Analysis")

        fig, ax = plt.subplots()
        ax.bar(df["Product"], df["Value"])
        ax.set_xlabel("Products")
        ax.set_ylabel("Value")
        st.pyplot(fig)

        st.subheader("Budget Usage")

        total_cost = sum([p[1] for p in products])
        usage = min(total_cost / budget, 1.0)

        st.progress(usage)

st.markdown("---")
st.markdown("OptiCart Pro | Advanced Shopping Optimization System")
