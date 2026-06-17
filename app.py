import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Medical Store Management",
    page_icon="💊",
    layout="wide"
)

# ---------------- LOGIN PAGE ----------------

USERNAME = "admin"
PASSWORD = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("💊 Medical Store Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    st.stop()

# ---------------- DATASET ----------------

data = {
    "Medicine_ID": ["M101","M102","M103","M104","M105","M106","M107","M108","M109","M110",
                    "M111","M112","M113","M114","M115","M116","M117","M118","M119","M120",
                    "M121","M122","M123","M124","M125","M126","M127","M128","M129","M130"],

    "Medicine_Name": ["Paracetamol","Crocin","Dolo 650","Ibuprofen","Cetirizine","Azithromycin",
                      "Amoxicillin","ORS","Cough Syrup","Antacid","Vitamin C","Calcium Tablets",
                      "Insulin","Glucometer","Bandage","Hand Sanitizer","Face Mask","BP Monitor",
                      "Thermometer","Eye Drops","Pain Relief Spray","Ayurvedic Oil",
                      "Protein Powder","Multivitamin","Burn Cream","Nasal Spray",
                      "Steam Inhaler","Glucose Powder","Digene","Liv 52"],

    "Category": ["Fever","Fever","Fever","Pain Relief","Allergy","Antibiotic","Antibiotic",
                 "Powder","Cough","Digestion","Vitamins","Vitamins","Diabetes","Diabetes",
                 "First Aid","Hygiene","Hygiene","Equipment","Equipment","Eye Care",
                 "Pain Relief","Ayurvedic","Supplement","Supplement","First Aid",
                 "Cold","Equipment","Energy Drink","Digestion","Liver Care"],

    "Stock": [120,80,95,70,60,45,50,150,55,85,100,90,25,35,200,75,180,20,40,65,
              50,70,30,85,60,45,25,100,90,55],

    "Price": [25,30,35,40,20,150,90,30,120,65,75,180,450,950,15,99,10,1800,250,
              85,160,140,1200,220,110,130,850,50,35,145],

    "Monthly_Sales": [320,280,350,210,190,130,160,240,110,175,220,145,95,60,410,
                      185,300,45,70,125,135,100,55,165,115,90,40,200,230,120]
}

df = pd.DataFrame(data)

# ---------------- SIDEBAR ----------------

st.sidebar.title("💊 Medical Store")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.header("Filters")

category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

search = st.sidebar.text_input("Search Medicine")

# ---------------- FILTERING ----------------

filtered_df = df.copy()

if category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category]

if search:
    filtered_df = filtered_df[
        filtered_df["Medicine_Name"].str.contains(search, case=False)
    ]

# ---------------- DASHBOARD ----------------

st.title("💊 Medical Store Management System")

col1, col2, col3 = st.columns(3)

col1.metric("Total Medicines", len(df))
col2.metric("Total Stock", df["Stock"].sum())
col3.metric("Total Monthly Sales", df["Monthly_Sales"].sum())

st.subheader("📋 Medicine Details")
st.dataframe(filtered_df, use_container_width=True)

st.subheader("⚠️ Low Stock Medicines (Stock < 50)")
low_stock = df[df["Stock"] < 50]
st.dataframe(low_stock, use_container_width=True)

st.subheader("📈 Top Selling Medicines")
top_sales = df.sort_values(by="Monthly_Sales", ascending=False).head(10)
st.bar_chart(top_sales.set_index("Medicine_Name")["Monthly_Sales"])

st.subheader("📊 Category Wise Stock")
category_stock = df.groupby("Category")["Stock"].sum()
st.bar_chart(category_stock)

st.success("✅ Medical Store Management Dashboard Loaded Successfully!")
