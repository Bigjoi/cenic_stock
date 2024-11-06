import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# แสดงหัวข้อหลัก
st.title('เครื่องมือแสดงผลการคำนวณและกราฟ')

# รับค่าจากผู้ใช้
st.header('กรอกข้อมูลที่นี่')
number = st.slider('เลือกจำนวน', min_value=0, max_value=100, value=50)

# คำนวณผลลัพธ์
result = np.sqrt(number)  # คำนวณรากที่สอง

# แสดงผลลัพธ์
st.write(f'ผลลัพธ์ของการคำนวณคือ: {result:.2f}')

# แสดงกราฟ
x = np.linspace(0, 10, 100)
y = np.sin(x)

st.subheader('กราฟของฟังก์ชัน sin(x)')
fig, ax = plt.subplots()
ax.plot(x, y)
st.pyplot(fig)

# แสดงข้อความเมื่อกดปุ่ม
if st.button('กดเพื่อแสดงข้อความ'):
    st.write('คุณกดปุ่มแล้ว!')
