import streamlit as st
import pandas as pd

# กำหนดชื่อไฟล์สำหรับบันทึกข้อมูล
DATA_FILE = 'stock_data.csv'

# ฟังก์ชันสำหรับโหลดข้อมูล
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Product", "Quantity", "Category", "Image"])

# ฟังก์ชันสำหรับบันทึกข้อมูล
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ตั้งค่า Streamlit
st.title('Stock Management System')

# โหลดข้อมูล
data = load_data()

# แสดงตาราง
st.write("Current Stock:")
st.dataframe(data)

# ฟอร์มสำหรับเพิ่มสินค้า
with st.form(key='add_product_form'):
    product = st.text_input("Product Name:")
    quantity = st.number_input("Quantity:", min_value=1, value=1)
    category = st.text_input("Category:")
    image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button(label='Add')

    if submit_button:
        if product and category and image:
            new_data = pd.DataFrame([[product, quantity, category, image.name]], columns=["Product", "Quantity", "Category", "Image"])
            data = pd.concat([data, new_data], ignore_index=True)
            save_data(data)
            
            # บันทึกรูปภาพในโฟลเดอร์
            with open(image.name, "wb") as f:
                f.write(image.getbuffer())
            
            st.success(f"Added {quantity} of {product} in category {category}")

# ฟอร์มสำหรับลดจำนวนสินค้า
with st.form(key='remove_product_form'):
    remove_product = st.selectbox("Select Product to Remove:", data['Product'].values)
    remove_quantity = st.number_input("Remove Quantity:", min_value=1, value=1)
    remove_button = st.form_submit_button(label='Remove')

    if remove_button:
        if remove_product in data['Product'].values:
            data.loc[data['Product'] == remove_product, 'Quantity'] -= remove_quantity
            data.loc[data['Quantity'] < 0, 'Quantity'] = 0  # ป้องกันไม่ให้จำนวนติดลบ
            save_data(data)
            st.success(f"Removed {remove_quantity} of {remove_product}")

# อัปเดตตาราง
st.write("Updated Stock:")
st.dataframe(data)

# แสดงรูปภาพสินค้า
for index, row in data.iterrows():
    st.subheader(row['Product'])
    st.image(row['Image'])
    st.write(f"Category: {row['Category']}, Quantity: {row['Quantity']}")
