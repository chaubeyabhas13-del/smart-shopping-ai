import streamlit as st
import pandas as pd

st.set_page_config(page_title="OptiCart Pro", layout="wide")

# 🎨 UI DESIGN
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #f5f7fa, #e4ecf7);
}
.card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.product-card {
    background: white;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
}
.stButton>button {
    background: #1a237e;
    color: white;
    border-radius: 8px;
    height: 45px;
}
</style>
""", unsafe_allow_html=True)

# 🏷️ TITLE
st.title("OptiCart Pro – Smart Shopping Optimization System")

# 📊 SIDEBAR
st.sidebar.header("Budget Settings")
budget = st.sidebar.number_input("Enter Budget ₹", min_value=1)

num_products = st.sidebar.slider("Number of Products", 1, 10, 3)

# 🛒 SESSION CART
if "cart" not in st.session_state:
    st.session_state.cart = []

# 🧭 TABS
tab1, tab2, tab3 = st.tabs(["Product Entry", "Shopping View", "Cart"])

products = []

# ------------------ TAB 1 ------------------
with tab1:
    st.subheader("Enter Product Details")

    for i in range(num_products):
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            name = st.text_input(f"Product {i+1}", key=f"name{i}")
        with col2:
            price = st.number_input(f"Price ₹{i+1}", key=f"price{i}")
        with col3:
            value = st.number_input(f"Rating {i+1}", key=f"value{i}")
        with col4:
            discount = st.slider(f"Discount %", 0, 50, key=f"disc{i}")
        with col5:
            image = st.text_input("Image URL", key=f"img{i}")

        final_price = price - (price * discount / 100)

        st.write(f"Final Price: ₹ {round(final_price,2)}")

        st.markdown("</div>", unsafe_allow_html=True)

        products.append({
            "name": name,
            "price": final_price,
            "value": value,
            "image": image
        })

# ------------------ TAB 2 ------------------
with tab2:
    st.subheader("Shopping View (Like Amazon)")

    cols = st.columns(3)

    for i, product in enumerate(products):
        with cols[i % 3]:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)

            if product["image"]:
                st.image(product["image"], height=150)

            st.write(f"**{product['name']}**")
            st.write(f"₹ {round(product['price'],2)}")
            st.write(f"Rating: {product['value']}")

            if st.button("Add to Cart", key=f"add{i}"):
                st.session_state.cart.append(product)

            st.markdown("</div>", unsafe_allow_html=True)

# ------------------ TAB 3 ------------------
with tab3:
    st.subheader("Your Cart")

    total = 0

    if len(st.session_state.cart) == 0:
        st.info("Cart is empty")
    else:
        for i, item in enumerate(st.session_state.cart):
            col1, col2, col3 = st.columns([1,3,1])

            with col1:
                if item["image"]:
                    st.image(item["image"], width=80)

            with col2:
                st.write(item["name"])
                st.write(f"₹ {round(item['price'],2)}")

            with col3:
                if st.button("Remove", key=f"remove{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()

            total += item["price"]

        st.markdown("---")
        st.subheader(f"Total: ₹ {round(total,2)}")

        # 🧠 Optimization suggestion
        if total > budget:
            st.error("Over Budget! Reduce items.")
        else:
            st.success("Within Budget ✅")

st.markdown("---")
st.markdown("OptiCart Pro | Advanced Smart Shopping System")
