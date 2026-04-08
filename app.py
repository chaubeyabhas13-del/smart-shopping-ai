import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="OptiCart Pro", layout="wide")

# ---------------- STYLING ----------------
st.markdown("""
<style>
body {
    background-color: #0b1a2f;
}

.main {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: white;
    padding: 20px;
    border-radius: 10px;
}

.card {
    background: white;
    color: black;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    margin-bottom: 15px;
}

button[kind="primary"] {
    background-color: #1e88e5;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "products" not in st.session_state:
    st.session_state.products = []

if "cart" not in st.session_state:
    st.session_state.cart = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("Budget Settings")

budget = st.sidebar.number_input("Enter Budget ₹", value=10000)

num_products = st.sidebar.slider("Number of Products", 1, 10, 3)

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align:center;'>OptiCart Pro – Smart Shopping Optimization System</h1>", unsafe_allow_html=True)

tabs = st.tabs(["Product Entry", "Shopping View", "Cart"])

# ================= PRODUCT ENTRY =================
with tabs[0]:
    st.subheader("Enter Product Details")

    products = []

    for i in range(num_products):
        st.markdown(f"### Product {i+1}")

        col1, col2, col3, col4 = st.columns(4)

        name = col1.text_input(f"Name {i}", key=f"name_{i}")
        price = col2.number_input(f"Price {i}", min_value=0.0, key=f"price_{i}")
        rating = col3.slider(f"Rating {i}", 1.0, 5.0, 4.0, key=f"rating_{i}")
        discount = col4.slider(f"Discount % {i}", 0, 50, 10, key=f"discount_{i}")

        final_price = price * (1 - discount / 100)

        st.write(f"Final Price: ₹ {round(final_price, 2)}")

        if name:
            products.append({
                "name": name,
                "price": price,
                "rating": rating,
                "discount": discount,
                "final_price": final_price
            })

    if st.button("Save Products"):
        st.session_state.products = products
        st.success("Products Saved!")

# ================= SHOPPING VIEW =================
with tabs[1]:
    st.subheader("Shopping View")

    if not st.session_state.products:
        st.warning("No products added yet!")
    else:
        cols = st.columns(3)

        for i, product in enumerate(st.session_state.products):
            with cols[i % 3]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                st.subheader(product["name"])
                st.write(f"Price: ₹ {round(product['final_price'], 2)}")
                st.write(f"Rating: ⭐ {product['rating']}")

                # ADD TO CART (FIXED)
                if st.button(f"Add {product['name']} to Cart", key=f"cart_{i}"):

                    # prevent duplicate
                    if product not in st.session_state.cart:
                        st.session_state.cart.append(product)
                        st.success(f"{product['name']} added to cart!")
                    else:
                        st.warning("Already in cart!")

                st.markdown("</div>", unsafe_allow_html=True)

# ================= CART =================
with tabs[2]:
    st.subheader("Your Cart")

    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        total = 0

        for item in st.session_state.cart:
            st.write(f"{item['name']} - ₹ {round(item['final_price'], 2)}")
            total += item["final_price"]

        st.markdown(f"### Total: ₹ {round(total, 2)}")

        if total > budget:
            st.error("Budget Exceeded!")
        else:
            st.success("Within Budget")

        # CLEAR CART BUTTON
        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.success("Cart cleared!")
