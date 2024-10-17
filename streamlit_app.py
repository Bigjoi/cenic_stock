import streamlit as st
import pandas as pd
import os

DATA_FILE = 'stock_data.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        data = {
            'รหัสสินค้า': ['SKU001', 'SKU002', 'SKU003'],
            'ชื่อสินค้า': ['สินค้า A', 'สินค้า B', 'สินค้า C'],
            'จำนวน': [10, 5, 8],
            'รูปภาพ': ['NC0000121 Ni-H Rechargeable Battery Unit.jpg'] * 3,
            'หมวดหมู่': ['หมวด A', 'หมวด B', 'หมวด A']
        }
        return pd.DataFrame(data)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

def update_stock(index, change):
    df.at[index, 'จำนวน'] += change
    save_data(df)
    if change > 0:
        st.success(f"เพิ่มสินค้า {df.at[index, 'ชื่อสินค้า']} จำนวน {change} ชิ้นแล้ว!")
    else:
        st.success(f"ลดสินค้า {df.at[index, 'ชื่อสินค้า']} จำนวน {abs(change)} ชิ้นแล้ว!")

def add_product(sku, name, quantity, image, category):
    global df
    new_product = {
        'รหัสสินค้า': sku,
        'ชื่อสินค้า': name,
        'จำนวน': quantity,
        'รูปภาพ': image,
        'หมวดหมู่': category
    }
    df = df.append(new_product, ignore_index=True)
    save_data(df)
    st.success(f"เพิ่มสินค้าใหม่: {name} สำเร็จแล้ว!")

st.title('โปรแกรมจัดการสต๊อกสินค้า')

# ฟอร์มเพิ่มสินค้าใหม่
st.header('เพิ่มรายการสินค้าใหม่')

with st.form(key='add_product_form'):
    sku = st.text_input('รหัสสินค้า')
    name = st.text_input('ชื่อสินค้า')
    quantity = st.number_input('จำนวนสินค้า', min_value=0)
    image = st.text_input('รูปภาพ (ชื่อไฟล์)')
    category = st.selectbox('หมวดหมู่', df['หมวดหมู่'].unique())

    submit_button = st.form_submit_button(label='เพิ่มสินค้า')
    if submit_button:
        add_product(sku, name, quantity, image, category)

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
