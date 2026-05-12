import streamlit as st
import datetime
import os
from Outlet_Project_Files.order import Order

# Constants
DATA_DIR = "Outlet_Project_Files"
HISTORY_FILE = "order_history.txt"
RECEIPT_FILE = "receipt.txt"

# Brand mapping (file names)
BRANDS = {
    "Monster": "monster.txt",
    "Redbull": "redbull.txt",
    "Celsius": "celsius.txt",
    "Reign": "reign.txt",
    "C4": "cfour.txt"
}


def load_drinks(brand):
    """Load drinks and prices from brand file."""
    file_path = os.path.join(DATA_DIR, BRANDS[brand])
    drinks = {}
    try:
        with open(file_path, "r") as f:
            for line in f:
                if "," in line:
                    drink, price = line.strip().split(",", 1)
                    drinks[drink.strip()] = float(price.strip())
    except FileNotFoundError:
        st.error(f"Drink file for {brand} not found.")
    except ValueError:
        st.error(f"Invalid price format in {brand} file.")
    return drinks


def save_order_history(name, price):
    """Save order to history file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(HISTORY_FILE, "a") as f:
            f.write(f"{name},{timestamp},${price:.2f}\n")
    except Exception as e:
        st.error(f"Error saving history: {e}")


def load_order_history():
    """Load order history from file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    history = []
    try:
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    name, timestamp, price = parts
                    history.append({
                        "name": name,
                        "timestamp": timestamp,
                        "price": price
                    })
    except Exception as e:
        st.error(f"Error loading history: {e}")
    return history


def update_order_history(history):
    """Update history file with edited data."""
    try:
        with open(HISTORY_FILE, "w") as f:
            for item in history:
                f.write(
                    f"{item['name']},{item['timestamp']},{item['price']}\n"
                )
    except Exception as e:
        st.error(f"Error updating history: {e}")


def trim_user_history(history, user_name):
    """Keep only the most recent finalized order's entries for a specific
    user."""
    user_name_lower = user_name.lower()
    user_entries = [
        item for item in history
        if item['name'].lower() == user_name_lower
    ]
    if not user_entries:
        return history, []

    # Find the most recent timestamp
    most_recent_timestamp = max(
        item['timestamp'] for item in user_entries
    )
    most_recent_entries = [
        item for item in user_entries
        if item['timestamp'] == most_recent_timestamp
    ]

    # Remove older entries for this user
    old_entries = set(
        (item['name'], item['timestamp'], item['price'])
        for item in user_entries
        if item['timestamp'] != most_recent_timestamp
    )
    cleaned_history = [
        item for item in history
        if not (
            item['name'].lower() == user_name_lower
            and (item['name'], item['timestamp'], item['price']) in old_entries
        )
    ]
    return cleaned_history, most_recent_entries


def generate_receipt(name, orders, timestamp):
    """Generate receipt file and return content."""
    total = sum(order.get_price() for order in orders)
    receipt_content = f"""---------Energy Outlet---------
-------------------------------
Name: {name}
Date: {timestamp}
-------------------------------
"""
    for order in orders:
        receipt_content += (
            f"{order.get_drink()} ({order.get_brand()}): "
            f"${order.get_price():.2f}\n"
        )
    receipt_content += (
        f"""-------------------------------
   TOTAL: ${total:.2f}
------Enjoy your beverage!------
"""
    )
    try:
        with open(RECEIPT_FILE, "w") as f:
            f.write(receipt_content)
    except Exception as e:
        st.error(f"Error writing receipt: {e}")
    return receipt_content


# Streamlit App
st.title("Energy Outlet Order System")

# Initialize session state
if "cart" not in st.session_state:
    st.session_state.cart = []
if "receipt" not in st.session_state:
    st.session_state.receipt = None
if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

# Sidebar navigation and customer input
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Order", "History"], index=0)

st.sidebar.title("Customer")
customer_name = st.sidebar.text_input(
    "Customer Name", value=st.session_state.customer_name
)
st.session_state.customer_name = customer_name

if page == "Order":
    st.header("Place Your Order")

    if not st.session_state.customer_name.strip():
        st.warning(
            "Please enter your name in the sidebar before ordering."
        )
    else:
        col1, col2 = st.columns(2)

        with col1:
            brand = st.selectbox("Choose Brand", list(BRANDS.keys()))

        with col2:
            if brand:
                drinks = load_drinks(brand)
                if drinks:
                    drink_options = list(drinks.keys())
                    selected_drink = st.selectbox(
                        "Choose Drink", drink_options
                    )

                    if selected_drink:
                        price = drinks[selected_drink]
                        st.write(f"Price: ${price:.2f}")

                        if st.button("Add to Order"):
                            order = Order(
                                st.session_state.customer_name,
                                brand, selected_drink, price
                            )
                            st.session_state.cart.append(order)
                            st.success(
                                f"Added {selected_drink} to cart!"
                            )
                            st.rerun()
                else:
                    st.error("No drinks available for this brand.")

        if st.session_state.cart:
            st.header("Your Order")
            total = 0
            for i, order in enumerate(st.session_state.cart):
                st.write(f"{i+1}. {order.summary()}")
                total += order.get_price()

            st.write(f"**Total: ${total:.2f}**")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Finalize Order"):
                    if st.session_state.cart:
                        for order in st.session_state.cart:
                            save_order_history(
                                order.get_customer_name(),
                                order.get_price()
                            )

                        timestamp = datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        receipt = generate_receipt(
                            st.session_state.cart[0].get_customer_name(),
                            st.session_state.cart, timestamp
                        )
                        st.session_state.receipt = receipt
                        st.session_state.cart = []
                        st.success(
                            "Order finalized successfully!"
                        )
                        st.rerun()
            with col2:
                if st.button("Clear order"):
                    st.session_state.cart = []
                    st.rerun()

        if st.session_state.receipt:
            st.header("Receipt")
            st.code(st.session_state.receipt, language="text")

elif page == "History":
    st.header("Order History")

    if not st.session_state.customer_name.strip():
        st.warning(
            "Please enter your name in the sidebar to view your history."
        )
    else:
        history = load_order_history()
        cleaned_history, user_history = trim_user_history(
            history, st.session_state.customer_name
        )
        if len(cleaned_history) != len(history):
            update_order_history(cleaned_history)
            history = cleaned_history

        if user_history:
            st.subheader(
                f"Most Recent Order for {st.session_state.customer_name}"
            )
            for i, item in enumerate(user_history):
                col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
                with col1:
                    st.write(f"{i+1}. **{item['name']}**")
                with col2:
                    st.write(item['timestamp'])
                with col3:
                    st.write(item['price'])
                with col4:
                    if st.button(f"Edit Name {i+1}", key=f"edit_{i}"):
                        st.session_state.edit_index = i

            if "edit_index" in st.session_state:
                idx = st.session_state.edit_index
                item = user_history[idx]

                st.subheader(f"Edit Order #{idx + 1}")
                with st.form(f"edit_form_{idx}"):
                    new_name = st.text_input(
                        "Customer Name", value=item['name']
                    )
                    st.write(f"Date/Time: {item['timestamp']}")
                    st.write(f"Price: {item['price']}")

                    col1, col2 = st.columns(2)
                    with col1:
                        submitted = st.form_submit_button("Save Name")
                    with col2:
                        if st.form_submit_button("Cancel"):
                            del st.session_state.edit_index
                            st.rerun()

                    if submitted:
                        original_idx = history.index(item)
                        history[original_idx] = {
                            "name": new_name,
                            "timestamp": item['timestamp'],
                            "price": item['price']
                        }
                        update_order_history(history)
                        del st.session_state.edit_index
                        st.success("Name updated!")
                        st.rerun()
        else:
            st.write("No order history found for your name.")
