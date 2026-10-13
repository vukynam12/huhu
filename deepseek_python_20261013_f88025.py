# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Cấu hình trang
st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Ứng dụng Quản lý Điểm Sinh viên")

# ==================== DỮ LIỆU MẪU ====================
@st.cache_data
def load_data():
    data = {
        "Họ và tên": [
            "Nguyễn Văn A", "Trần Thị B", "Lê Văn C", "Phạm Thị D", "Hoàng Văn E",
            "Huỳnh Thị F", "Phan Văn G", "Võ Thị H", "Đặng Văn I", "Bùi Thị K"
        ],
        "Tong_ket": [8.5, 7.2, 5.0, 9.0, 3.5, 6.8, 8.2, 4.5, 7.8, 9.5],
        "Xep_loai": [
            "Giỏi", "Khá", "Trung bình", "Giỏi", "Yếu",
            "Khá", "Giỏi", "Yếu", "Khá", "Giỏi"
        ]
    }
    return pd.DataFrame(data)

df = load_data()

# ==================== 4. BIỂU ĐỒ ====================
st.subheader("4. Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(df["Họ và tên"], df["Tong_ket"], color="cornflowerblue")
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Tên sinh viên")
ax.set_xlim(0, 10)

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ==================== 5. TÌM KIẾM & LỌC ====================
st.subheader("5. Tìm kiếm và lọc sinh viên")

col1, col2 = st.columns(2)
with col1:
    tu_khoa = st.text_input("Nhập họ tên sinh viên")
with col2:
    loai = st.selectbox(
        "Chọn xếp loại",
        ["Tất cả", "Giỏi", "Khá", "Trung bình", "Yếu"]
    )

ket_qua = df.copy()

if tu_khoa.strip():
    ket_qua = ket_qua[
        ket_qua["Họ và tên"].str.contains(tu_khoa, case=False, na=False)
    ]

if loai != "Tất cả":
    ket_qua = ket_qua[ket_qua["Xep_loai"] == loai]

st.dataframe(ket_qua, use_container_width=True, hide_index=True)

# ==================== 6. TẢI FILE ====================
st.subheader("6. Tải bảng điểm")

col_csv, col_xlsx = st.columns(2)

# Tải CSV
with col_csv:
    csv_data = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Tải bảng điểm CSV",
        data=csv_data,
        file_name="bang_diem_sinh_vien.csv",
        mime="text/csv",
        use_container_width=True
    )

# Tải Excel
with col_xlsx:
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Bang diem")

    st.download_button(
        "⬇️ Tải bảng điểm Excel",
        data=excel_buffer.getvalue(),
        file_name="bang_diem_sinh_vien.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# ==================== 8. THÔNG TIN ====================
st.divider()
st.markdown(
    """
    <div style="text-align:center; font-size:12px; color:gray;">
        Người tạo: Phùng Thanh Mai<br>
        MSSV: 026308010392
    </div>
    """,
    unsafe_allow_html=True
)