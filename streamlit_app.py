import streamlit as st
import pandas as pd
from PIL import Image

# สร้าง DataFrame สำหรับสินค้าคงคลัง
data = {
    'รหัสสินค้า': ['SKU001', 'SKU002', 'SKU003'],
    'ชื่อสินค้า': ['สินค้า A', 'สินค้า B', 'สินค้า C'],
    'จำนวน': [10, 5, 8],
    'รูปภาพ': ['NC0000121 Ni-H Rechargeable Battery Unit.jpg', 'NC0000121 Ni-H Rechargeable Battery Unit.jpg', 'NC0000121 Ni-H Rechargeable Battery Unit.jpg']
}

# สร้าง DataFrame
df = pd.DataFrame(data)

# ฟังก์ชันเพื่อเพิ่มหรือลดจำนวนสินค้า
def update_stock(index, change):
    df.at[index, 'จำนวน'] += change

# แสดงชื่อสินค้าและข้อมูล
st.title('โปรแกรมจัดการสต๊อกสินค้า')

for index, row in df.iterrows():
    st.header(row['ชื่อสินค้า'])
    st.image(row['รูปภาพ'], width=150)
    st.write(f"รหัสสินค้า: {row['รหัสสินค้า']}")
    st.write(f"จำนวนสินค้า: {row['จำนวน']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button('เพิ่ม', key=f'add_{index}'):
            update_stock(index, 1)
    with col2:
        if st.button('ลด', key=f'remove_{index}'):
            update_stock(index, -1)

# แสดงข้อมูลสต๊อกสินค้าปัจจุบัน
st.write(df)
