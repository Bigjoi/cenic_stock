import streamlit as st
import pandas as pd
import os

# กำหนดชื่อไฟล์สำหรับบันทึกข้อมูล
DATA_FILE = 'stock_data.csv'

# ฟังก์ชันโหลดข้อมูล
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # ถ้าไม่มีไฟล์ให้สร้าง DataFrame ใหม่
        data = {
            'รหัสสินค้า': ['SKU001', 'SKU002', 'SKU003'],
            'ชื่อสินค้า': ['สินค้า A', 'สินค้า B', 'สินค้า C'],
            'จำนวน': [10, 5, 8],
            'รูปภาพ': ['NC0000121 Ni-H Rechargeable Battery Unit.jpg', 'NC0000121 Ni-H Rechargeable Battery Unit.jpg', 'NC0000121 Ni-H Rechargeable Battery Unit.jpg'],
            'หมวดหมู่': ['หมวด A', 'หมวด B', 'หมวด A']
        }
        return pd.DataFrame(data)

# ฟังก์ชันบันทึกข้อมูล
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# โหลดข้อมูลเมื่อเริ่มโปรแกรม
df = load_data()

# ฟังก์ชันเพื่อเพิ่มหรือลดจำนวนสินค้า
def update_stock(index, change):
    df.at[index, 'จำนวน'] += change
    save_data(df)  # บันทึกข้อมูลหลังจากปรับปรุง

# แสดงชื่อสินค้าและข้อมูล
st.title('โปรแกรมจัดการสต๊อกสินค้า')

# ตัวกรองหมวดหมู่
categories = df['หมวดหมู่'].unique()
selected_category = st.selectbox('เลือกหมวดหมู่:', ['ทั้งหมด'] + list(categories))

# แสดงข้อมูลตามหมวดหมู่ที่เลือก
if selected_category != 'ทั้งหมด':
    filtered_df = df[df['หมวดหมู่'] == selected_category]
else:
    filtered_df = df

# แสดงรายการสินค้า
for index, row in filtered_df.iterrows():
    st.header(row['ชื่อสินค้า'])
    st.image(row['รูปภาพ'], width=150)
    st.write(f"รหัสสินค้า: {row['รหัสสินค้า']}")
    st.write(f"จำนวนสินค้า: {row['จำนวน']}")
    st.write(f"หมวดหมู่: {row['หมวดหมู่']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button('เพิ่ม', key=f'add_{index}'):
            update_stock(index, 1)
    with col2:
        if st.button('ลด', key=f'remove_{index}'):
            update_stock(index, -1)

# แสดงข้อมูลสต๊อกสินค้าปัจจุบัน
st.write("ข้อมูลสต๊อกสินค้าทั้งหมด:")
st.write(df)
