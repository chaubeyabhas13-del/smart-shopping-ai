import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="OptiCart Pro", layout="wide")

# ---------------- NEW PREMIUM UI ----------------
st.markdown("""
<style>

/* 🌌 Full App Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* 📦 Sidebar */
[data-testid="stSidebar"] {
    background-color: #0b1a2f;
    color: white;
}

/* ✨ Titles */
h1 {
    color: #ffffff;
    font-weight: 700;
}

h2, h3 {
    color: #e3f2fd;
}

/* 🧾 Cards */
.card {
    background: white;
    color: #1a1a1a;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.25);
    transition: transform 0.2s ease;
}

.card:hover {
    transform: scale(1.03);
}

/* 🔘 Buttons */
button[kind="primary"] {
    background: linear-gradient(135deg, #2196f3, #21cbf3);
    color: white;
    border-radius: 8px;
    font-weight: 600;
}

/* 💡 Inputs */
input, .stNumberInput, .stTextInput {
    background-color: #f5f7fa !important;
    border-radius: 8px !important;
}

/* 📊 Tabs */
button[data-baseweb="tab"] {
    font-weight: 600;
    color: #bbdefb;
}

button[aria-selected="true"] {
    color: #ffffff !important;
    border-bottom: 3px solid #4fc3f7;
}

/* 📦 Alerts */
.stAlert {
    border-radius: 10px;
}

/* 🔥 Spacing */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
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

tabs = st.tabs(["Product Entry", "Shopping View", "Cart", "Smart Analysis"])

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

        if name.strip() != "" and price > 0:
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

                st.subheader(product.get("name", "No Name"))
                st.write(f"Price: ₹ {round(product.get('final_price', 0), 2)}")
                st.write(f"Rating: ⭐ {product.get('rating', 0)}")

                if st.button(f"Add {product['name']} to Cart", key=f"cart_{i}"):
                    if product not in st.session_state.cart:
                        st.session_state.cart.append(product)
                        st.success("Added!")
                    else:
                        st.warning("Already in cart")

                st.markdown("</div>", unsafe_allow_html=True)

# ================= CART =================
with tabs[2]:
    st.subheader("Your Cart")

    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        total = 0

        for item in st.session_state.cart:
            price = item.get("final_price", 0)
            st.write(f"{item.get('name')} - ₹ {round(price, 2)}")
            total += price

        st.markdown(f"### Total: ₹ {round(total, 2)}")

        if total > budget:
            st.error("Budget Exceeded!")
        else:
            st.success("Within Budget")

        if st.button("Clear Cart"):
            st.session_state.cart = []

# ================= SMART ANALYSIS =================
with tabs[3]:
    st.subheader("Smart Analysis")

    if not st.session_state.products:
        st.warning("Add products first!")
    else:
        valid_products = [
            p for p in st.session_state.products
            if "rating" in p and "final_price" in p
        ]

        if not valid_products:
            st.error("No valid products available!")
        else:
            best = max(
                valid_products,
                key=lambda x: x.get("rating", 0) / (x.get("final_price", 1) + 1)
            )

            st.success(f"Best Value Product: {best['name']}")

            st.write("✔ High rating compared to price")
            st.write("✔ Best value for money")
