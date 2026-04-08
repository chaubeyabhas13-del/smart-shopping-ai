import streamlit as st
import pandas as pd

st.set_page_config(page_title="OptiCart Pro", layout="wide")

# 🎨 PREMIUM UI (FIXED VISIBILITY)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #ffffff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0b0b0b;
    color: white;
}

/* Inputs */
input, textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-radius: 8px !important;
}

div[data-baseweb="input"] {
    background-color: white !important;
    color: black !important;
}

/* Labels */
label {
    color: #ffffff !important;
    font-weight: 500;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
}

/* Product Cards */
.product-card {
    background: rgba(255,255,255,0.12);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    transition: 0.3s;
}
.product-card:hover {
    transform: scale(1.05);
}

/* Button */
.stButton>button {
    background: linear-gradient(45deg, #ff6a00, #ee0979);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
    border: none;
}

/* Headings */
h1, h2, h3 {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# 🏷️ TITLE
st.title("OptiCart Pro – Smart Shopping Optimization System")

# 📊 SIDEBAR
st.sidebar.header("Budget Settings")
budget = st.sidebar.number_input("Enter Budget ₹", min_value=1)
num_products = st.sidebar.slider("Number of Products", 1, 10, 3)

# 🛒 CART
if "cart" not in st.session_state:
    st.session_state.cart = []

# 🧭 TABS
tab1, tab2, tab3, tab4 = st.tabs(
    ["Product Entry", "Shopping View", "Cart", "Smart Analysis"]
)

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
    st.subheader("Shopping View")

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

        if total > budget:
            st.error("Over Budget! Reduce items.")
        else:
            st.success("Within Budget ✅")

# ------------------ TAB 4 ------------------
with tab4:
    st.subheader("Smart Recommendation System")

    valid_products = [p for p in products if p["name"] and p["price"] > 0]

    if len(valid_products) == 0:
        st.warning("Enter product details first")
    else:
        for p in valid_products:
            p["score"] = p["value"] / p["price"] if p["price"] > 0 else 0

        # 🏆 Best Product
        best = max(valid_products, key=lambda x: x["score"])
        st.success(f"Best Value Product: {best['name']}")

        # 💰 Budget Optimization
        sorted_products = sorted(valid_products, key=lambda x: x["score"], reverse=True)

        selected = []
        total = 0

        for p in sorted_products:
            if total + p["price"] <= budget:
                selected.append(p)
                total += p["price"]

        st.write("### Recommended Products Under Budget")

        for p in selected:
            st.write(f"{p['name']} - ₹{round(p['price'],2)}")

        st.write(f"Total: ₹{round(total,2)}")

        # 📊 Table
        df = pd.DataFrame(valid_products)
        st.dataframe(df[["name", "price", "value", "score"]])

# FOOTER
st.markdown("---")
st.markdown("OptiCart Pro | Advanced Smart Shopping System")
