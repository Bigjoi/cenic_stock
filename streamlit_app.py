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

# เลือกหมวดหมู่เพื่อกรองข้อมูล
selected_category = st.selectbox("Select Category to View:", ["All"] + data['Category'].unique().tolist())

if selected_category != "All":
    filtered_data = data[data['Category'] == selected_category]
else:
    filtered_data = data

# แสดงตาราง
st.write("Current Stock:")
st.dataframe(filtered_data)

# แสดงรูปภาพสินค้า
for index, row in filtered_data.iterrows():
    st.subheader(row['Product'])
    st.image(row['Image'])
    st.write(f"Category: {row['Category']}, Quantity: {row['Quantity']}")

# ฟอร์มสำหรับเพิ่มหรือลดจำนวนสินค้า
st.header("Update Product Quantity")
with st.form(key='update_product_form'):
    product = st.selectbox("Select Product:", data['Product'].values)
    quantity_change = st.number_input("Change Quantity (positive to add, negative to remove):", value=1)
    submit_button = st.form_submit_button(label='Update')

    if submit_button:
        if product in data['Product'].values:
            new_quantity = data.loc[data['Product'] == product, 'Quantity'].values[0] + quantity_change
            new_quantity = max(new_quantity, 0)  # ป้องกันไม่ให้จำนวนติดลบ
            data.loc[data['Product'] == product, 'Quantity'] = new_quantity
            save_data(data)
            st.success(f"Updated {product} quantity to {new_quantity}")

# ฟอร์มสำหรับเพิ่มสินค้า
st.header("Add New Product")
with st.form(key='add_product_form'):
    new_product = st.text_input("Product Name:")
    new_quantity = st.number_input("Quantity:", min_value=1, value=1)
    category = st.text_input("Category:")
    image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button(label='Add')

    if submit_button:
        if new_product and category and image:
            new_data = pd.DataFrame([[new_product, new_quantity, category, image.name]], columns=["Product", "Quantity", "Category", "Image"])
            data = pd.concat([data, new_data], ignore_index=True)
            save_data(data)
            
            # บันทึกรูปภาพในโฟลเดอร์
            with open(image.name, "wb") as f:
                f.write(image.getbuffer())
            
            st.success(f"Added {new_quantity} of {new_product} in category {category}")
