import streamlit as st
import pandas as pd

st.set_page_config(page_title="OptiCart Pro", layout="wide")

# 🎨 CLEAN UI
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: #ffffff;
}

section[data-testid="stSidebar"] {
    background: #0d1117;
    color: white;
}

input, textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-radius: 8px !important;
}

label {
    color: #ffffff !important;
    font-weight: 500;
}

.card {
    background: rgba(255,255,255,0.12);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.product-card {
    background: rgba(255,255,255,0.15);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

.stButton>button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
    border: none;
}

button[data-baseweb="tab"] {
    color: white !important;
}
button[aria-selected="true"] {
    border-bottom: 3px solid #00c6ff !important;
}

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

# ------------------ PRODUCT ENTRY ------------------
with tab1:
    st.subheader("Enter Product Details")

    default_products = [
        {"name": "iPhone 15", "price": 79999, "value": 4.8, "discount": 10,
         "image": "https://m.media-amazon.com/images/I/71d7rfSl0wL._SX679_.jpg"},
        {"name": "Nike Shoes", "price": 4999, "value": 4.5, "discount": 20,
         "image": "https://static.nike.com/a/images/t_PDP_936_v1/f_auto,q_auto:eco/air-max.jpg"},
        {"name": "Laptop", "price": 65000, "value": 4.6, "discount": 15,
         "image": "https://m.media-amazon.com/images/I/71vFKBpKakL._SX679_.jpg"},
        {"name": "Headphones", "price": 2999, "value": 4.3, "discount": 25,
         "image": "https://m.media-amazon.com/images/I/61CGHv6kmWL._SX679_.jpg"},
        {"name": "Smart Watch", "price": 6999, "value": 4.4, "discount": 18,
         "image": "https://m.media-amazon.com/images/I/61y2VVWcGBL._SX679_.jpg"},
    ]

    for i in range(num_products):
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        default = default_products[i] if i < len(default_products) else {
            "name": f"Product {i+1}",
            "price": 1000,
            "value": 4.0,
            "discount": 10,
            "image": ""
        }

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            name = st.text_input(f"Product {i+1}", value=default["name"], key=f"name{i}")
        with col2:
            price = st.number_input(f"Price ₹{i+1}", value=default["price"], key=f"price{i}")
        with col3:
            value = st.number_input(f"Rating {i+1}", value=default["value"], key=f"value{i}")
        with col4:
            discount = st.slider(f"Discount %", 0, 50, default["discount"], key=f"disc{i}")
        with col5:
            image = st.text_input("Image URL", value=default["image"], key=f"img{i}")

        final_price = price - (price * discount / 100)

        st.write(f"Final Price: ₹ {round(final_price,2)}")

        st.markdown("</div>", unsafe_allow_html=True)

        products.append({
            "name": name,
            "price": final_price,
            "value": value,
            "image": image
        })

# ------------------ SHOPPING VIEW ------------------
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

# ------------------ CART ------------------
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
            st.error("Over Budget!")
        else:
            st.success("Within Budget")

# ------------------ SMART ANALYSIS ------------------
with tab4:
    st.subheader("Smart Recommendation System")

    valid_products = [p for p in products if p["name"] and p["price"] > 0]

    if len(valid_products) == 0:
        st.warning("Enter product details first")
    else:
        for p in valid_products:
            p["score"] = p["value"] / p["price"]

        best = max(valid_products, key=lambda x: x["score"])
        st.success(f"Best Product: {best['name']}")

        sorted_products = sorted(valid_products, key=lambda x: x["score"], reverse=True)

        selected = []
        total = 0

        for p in sorted_products:
            if total + p["price"] <= budget:
                selected.append(p)
                total += p["price"]

        st.write("Recommended within budget:")
        for p in selected:
            st.write(f"{p['name']} - ₹{round(p['price'],2)}")

        df = pd.DataFrame(valid_products)
        st.dataframe(df[["name", "price", "value", "score"]])

# FOOTER
st.markdown("---")
st.markdown("OptiCart Pro | Advanced Smart Shopping System")
