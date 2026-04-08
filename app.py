import streamlit as st

st.set_page_config(page_title="OptiCart Pro", layout="wide")

# 🎨 FIXED PREMIUM UI (VISIBLE + CLEAN)
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #ffffff;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #0b0b0b;
    color: white;
}

/* INPUT BOXES */
input, textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-radius: 8px !important;
}

/* NUMBER INPUT */
div[data-baseweb="input"] {
    background-color: white !important;
    color: black !important;
}

/* LABELS */
label {
    color: #ffffff !important;
    font-weight: 500;
}

/* SLIDER */
.stSlider label {
    color: white !important;
}

/* CARDS */
.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

/* PRODUCT CARD */
.product-card {
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.3);
    transition: 0.3s;
}
.product-card:hover {
    transform: scale(1.05);
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(45deg, #ff6a00, #ee0979);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
    border: none;
}

/* HEADINGS */
h1, h2, h3 {
    color: #ffffff !important;
}

/* TEXT */
p {
    color: #e0e0e0;
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

# FOOTER
st.markdown("---")
st.markdown("OptiCart Pro | Advanced Smart Shopping System")
