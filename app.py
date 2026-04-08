import streamlit as st
import pandas as pd

st.set_page_config(page_title="OptiCart Pro", layout="wide")

# ---------- PREMIUM UI ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
}

section[data-testid="stSidebar"] {
    background-color: #0a0f1c;
    color: white;
}

h1, h2, h3 {
    color: white;
}

.card {
    background: white;
    color: black;
    padding: 15px;
    border-radius: 15px;
    margin: 10px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    text-align: center;
}

.stButton>button {
    background-color: #00c6ff;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("Budget Settings")

budget = st.sidebar.number_input("Enter Budget ₹", value=100000)

num_products = st.sidebar.slider("Number of Products", 1, 5, 3)

# ---------- TITLE ----------
st.title("OptiCart Pro – Smart Shopping Optimization System")

# ---------- DEFAULT IMAGES ----------
default_images = [
    "https://m.media-amazon.com/images/I/71d7rfSl0wL._SX679_.jpg",
    "https://static.nike.com/a/images/t_PDP_936_v1/f_auto,q_auto:eco/air-max.jpg",
    "https://m.media-amazon.com/images/I/71vFKBpKakL._SX679_.jpg",
    "https://m.media-amazon.com/images/I/81Zt42ioCgL._SX679_.jpg",
    "https://m.media-amazon.com/images/I/61bK6PMOC3L._SX679_.jpg"
]

# ---------- SESSION ----------
if "products" not in st.session_state:
    st.session_state.products = []

if "cart" not in st.session_state:
    st.session_state.cart = []

# ---------- TABS ----------
tab1, tab2, tab3, tab4 = st.tabs(
    ["Product Entry", "Shopping View", "Cart", "Smart Analysis"]
)

# ---------- PRODUCT ENTRY ----------
with tab1:
    st.header("Enter Product Details")

    products = []

    for i in range(num_products):
        st.subheader(f"Product {i+1}")

        col1, col2, col3, col4 = st.columns(4)

        name = col1.text_input("Name", key=f"name{i}")
        price = col2.number_input("Price", key=f"price{i}", value=0)
        rating = col3.number_input("Rating", 0.0, 5.0, key=f"rating{i}")
        discount = col4.slider("Discount %", 0, 50, key=f"discount{i}")

        final_price = round(price * (1 - discount / 100), 2)

        st.write(f"Final Price: ₹ {final_price}")

        products.append({
            "name": name,
            "price": final_price,
            "rating": rating,
            "image": default_images[i]
        })

    if st.button("Save Products"):
        st.session_state.products = products
        st.success("Products Saved Successfully!")

# ---------- SHOPPING VIEW ----------
with tab2:
    st.header("Shopping View")

    cols = st.columns(3)

    for idx, product in enumerate(st.session_state.products):
        with cols[idx % 3]:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.image(product["image"], height=150)

            st.subheader(product["name"])
            st.write(f"Price: ₹ {product['price']}")
            st.write(f"Rating: {product['rating']} ⭐")

            if st.button(f"Add to Cart {idx}"):
                st.session_state.cart.append(product)

            st.markdown('</div>', unsafe_allow_html=True)

# ---------- CART ----------
with tab3:
    st.header("Cart")

    total = 0

    if st.session_state.cart:
        for item in st.session_state.cart:
            st.write(f"{item['name']} - ₹{item['price']}")
            total += item["price"]

        total = round(total, 2)
        st.write(f"Total: ₹ {total}")

        if total > budget:
            st.error("Budget Exceeded!")
        else:
            st.success("Within Budget")
    else:
        st.write("Cart is empty")

# ---------- ANALYSIS ----------
with tab4:
    st.header("Smart Analysis")

    if st.session_state.products:
        df = pd.DataFrame(st.session_state.products)

        st.subheader("Top Rated Products")
        st.dataframe(df.sort_values(by="rating", ascending=False))

        df["score"] = df["rating"] / df["price"]

        st.subheader("Best Value Products")
        st.dataframe(df.sort_values(by="score", ascending=False))
    else:
        st.write("No data available")
