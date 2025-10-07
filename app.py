import streamlit as st
from datetime import date
from src.services.user_service import user_service
from src.services.wardrobe_service import wardrobe_service
from src.services.outfit_service import outfit_service
from src.services.plan_service import plan_service

st.set_page_config(page_title="Outfit Planner", page_icon="👗", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("👗 Outfit Planner")
page = st.sidebar.radio(
    "Navigate to:",
    ["Users", "Wardrobe", "Outfits", "Plans"]
)

# Ensure session state has current user
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# --- USERS PAGE ---
if page == "Users":
    st.title("👤 Manage Users")

    with st.expander("➕ Add or Login User"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        if st.button("Add / Login"):
            if name and email:
                result = user_service.add_user(name, email)
                if "message" in result and result["message"] == "User already exists":
                    st.warning(f"User already exists with ID {result['user']['id']}")
                    st.session_state.current_user = result["user"]
                else:
                    st.success("✅ User added successfully!")
                    st.session_state.current_user = result
            else:
                st.warning("Please fill in both name and email.")

    if st.session_state.current_user:
        st.subheader("🆕 Current User")
        st.table([{
            "id": st.session_state.current_user["id"],
            "name": st.session_state.current_user["name"],
            "email": st.session_state.current_user["email"]
        }])

# --- WARDROBE PAGE ---
elif page == "Wardrobe":
    st.title("👕 Manage Wardrobe")

    if not st.session_state.current_user:
        st.warning("Please add or login a user first.")
    else:
        user_id = st.session_state.current_user["id"]
        st.write(f"📌 Current User ID: {user_id}")

        with st.expander("➕ Add Wardrobe Item"):
            name = st.text_input("Item Name")
            type_ = st.text_input("Type (e.g., Shirt, Jeans, Saree)")
            color = st.text_input("Color")
            if st.button("Add Item"):
                if name and type_ and color:
                    item = wardrobe_service.add_item(user_id, name, color, type_)
                    st.success("✅ Wardrobe item added!")
                    st.json(item)
                else:
                    st.warning("Please fill in all fields.")

        st.subheader("👚 Wardrobe Items")
        if st.button("View Wardrobe Items"):
            items = wardrobe_service.list_items(user_id)
            if items:
                st.table(items)
            else:
                st.info("No wardrobe items found.")

        st.subheader("🔍 Search Wardrobe")
        keyword = st.text_input("Enter keyword to search")
        if st.button("Search Wardrobe"):
            results = wardrobe_service.search_items(user_id, keyword)
            if results:
                st.write("### Search Results")
                st.table(results)
            else:
                st.info("No matching items found.")

# --- OUTFITS PAGE ---
elif page == "Outfits":
    st.title("👗 Manage Outfits")

    if not st.session_state.current_user:
        st.warning("Please add or login a user first.")
    else:
        user_id = st.session_state.current_user["id"]
        st.write(f"📌 Current User ID: {user_id}")

        with st.expander("➕ Create Outfit"):
            name = st.text_input("Outfit Name")
            occasion = st.text_input("Occasion (optional)")
            item_ids_input = st.text_input("Enter Wardrobe Item IDs (comma separated)")
            if st.button("Create Outfit"):
                try:
                    item_ids = [int(i.strip()) for i in item_ids_input.split(",") if i.strip()]
                    outfit = outfit_service.add_outfit(user_id, name, occasion, item_ids)
                    st.success("✅ Outfit created!")
                    st.json(outfit)
                except Exception as e:
                    st.error(f"Error: {e}")

        st.subheader("📋 Your Outfits")
        if st.button("View Outfits"):
            outfits = outfit_service.list_outfits(user_id)
            if outfits:
                st.table(outfits)
            else:
                st.info("No outfits found.")

        st.subheader("🔍 Search Outfits")
        keyword = st.text_input("Search outfits by name or occasion")
        if st.button("Search Outfits"):
            results = outfit_service.search_outfits(user_id, keyword)
            if results:
                st.write("### Search Results")
                st.table(results)
            else:
                st.info("No matching outfits found.")

# --- PLANS PAGE ---
elif page == "Plans":
    st.title("🗓️ Outfit Plans")

    if not st.session_state.current_user:
        st.warning("Please add or login a user first.")
    else:
        user_id = st.session_state.current_user["id"]
        st.write(f"📌 Current User ID: {user_id}")

        with st.expander("📅 Schedule Outfit"):
            outfit_id = st.number_input("Outfit ID", min_value=1, step=1)
            date_input = st.date_input("Select Date", value=date.today())
            if st.button("Add Plan"):
                plan = plan_service.add_plan(user_id, outfit_id, str(date_input))
                st.success("✅ Plan added!")
                st.json(plan)

        st.subheader("🧾 Your Planned Outfits")
        if st.button("View Plans"):
            plans = plan_service.list_plans(user_id)
            if plans:
                st.table(plans)
            else:
                st.info("No plans found.")
