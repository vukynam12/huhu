# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# ==================== CẤU HÌNH TRANG ====================
st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="📊",
    layout="wide"
)

# ==================== HÀM TÍNH ĐIỂM & XẾP LOẠI ====================
def tinh_tong_ket(row):
    """Tong_ket = 10% CC + 30% GK + 60% CK"""
    return round(
        0.1 * row["Điểm chuyên cần"]
        + 0.3 * row["Điểm giữa kì"]
        + 0.6 * row["Điểm cuối kì"],
        2
    )

def xep_loai(diem):
    if diem >= 8.0:
        return "Giỏi"
    elif diem >= 6.5:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

# ==================== 1. GIỚI THIỆU ====================
st.title("📊 Ứng dụng Quản lý Điểm Sinh viên")

st.markdown("""
### 1. Giới thiệu
Ứng dụng này giúp **quản lý, phân tích và trực quan hóa điểm** của sinh viên.

**Các chức năng chính:**
- 📥 Nhập dữ liệu điểm sinh viên (nhập tay hoặc tải file CSV)
- 📈 Xem thống kê mô tả (điểm trung bình, cao nhất, thấp nhất,...)
- 📊 Xem biểu đồ điểm tổng kết
- 🔍 Tìm kiếm và lọc sinh viên theo tên / xếp loại
- 💾 Tải bảng điểm về máy dưới dạng CSV hoặc Excel

**Công thức tính điểm tổng kết:**
> `Tong_ket = 10% × Chuyên cần + 30% × Giữa kì + 60% × Cuối kì`
""")

st.divider()

# ==================== 2. NHẬP DỮ LIỆU ====================
st.subheader("2. Nhập dữ liệu sinh viên")

# ---------- Dữ liệu mẫu MỚI ----------
DEFAULT_DATA = {
    "Họ và tên": [
        "Nguyễn Văn An", "Lưu Thị Bình", "Chu Hoài Bảo", "Nguyễn Diệp Chi",
        "Phạm Khánh Văn", "Hoài Thị Phương", "Nguyễn Gia Tuấn",
        "Trần Kiều My", "Đinh Văn Nam", "Lương Ngọc Bích"
    ],
    "Điểm chuyên cần": [8, 10, 7, 9, 7, 9, 10, 9, 7, 10],
    "Điểm giữa kì":    [10, 8, 6, 9, 6, 7, 8, 8, 10, 8],
    "Điểm cuối kì":    [7, 8, 9, 10, 8, 9, 6, 5, 10, 7]
}

def build_df(raw: dict) -> pd.DataFrame:
    """Tạo DataFrame + tính Tong_ket + Xep_loai."""
    d = pd.DataFrame(raw)
    d["Tong_ket"] = d.apply(tinh_tong_ket, axis=1)
    d["Xep_loai"] = d["Tong_ket"].apply(xep_loai)
    return d

# Khởi tạo session_state
if "df" not in st.session_state:
    st.session_state.df = build_df(DEFAULT_DATA)

# Lựa chọn cách nhập
cach_nhap = st.radio(
    "Chọn cách nhập dữ liệu:",
    ["Dùng dữ liệu mẫu", "Tải file CSV lên", "Nhập trực tiếp"],
    horizontal=True
)

if cach_nhap == "Dùng dữ liệu mẫu":
    st.session_state.df = build_df(DEFAULT_DATA)
    st.info("✅ Đang dùng dữ liệu mẫu gồm 10 sinh viên.")

elif cach_nhap == "Tải file CSV lên":
    uploaded_file = st.file_uploader(
        "Chọn file CSV (cần cột: 'Họ và tên', 'Điểm chuyên cần', 'Điểm giữa kì', 'Điểm cuối kì')",
        type=["csv"]
    )
    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            required_cols = {
                "Họ và tên", "Điểm chuyên cần",
                "Điểm giữa kì", "Điểm cuối kì"
            }
            if required_cols.issubset(df_upload.columns):
                st.session_state.df = build_df(df_upload.to_dict("list"))
                st.success(f"✅ Đã tải {len(df_upload)} sinh viên từ file.")
            else:
                st.error(f"❌ File thiếu cột. Cần có: {required_cols}")
        except Exception as e:
            st.error(f"❌ Lỗi đọc file: {e}")

elif cach_nhap == "Nhập trực tiếp":
    with st.form("form_nhap"):
        st.write("Nhập thông tin sinh viên mới:")
        ho_ten = st.text_input("Họ và tên")
        c1, c2, c3 = st.columns(3)
        with c1:
            cc = st.number_input("Điểm chuyên cần", 0.0, 10.0, 8.0, 0.5)
        with c2:
            gk = st.number_input("Điểm giữa kì", 0.0, 10.0, 7.0, 0.5)
        with c3:
            ck = st.number_input("Điểm cuối kì", 0.0, 10.0, 7.0, 0.5)
        submitted = st.form_submit_button("➕ Thêm sinh viên")

        if submitted and ho_ten.strip():
            new_row = pd.DataFrame([{
                "Họ và tên": ho_ten,
                "Điểm chuyên cần": cc,
                "Điểm giữa kì": gk,
                "Điểm cuối kì": ck
            }])
            new_row["Tong_ket"] = new_row.apply(tinh_tong_ket, axis=1)
            new_row["Xep_loai"] = new_row["Tong_ket"].apply(xep_loai)
            st.session_state.df = pd.concat(
                [st.session_state.df, new_row], ignore_index=True
            )
            st.success(
                f"✅ Đã thêm: {ho_ten} — Tổng kết "
                f"{new_row['Tong_ket'].iloc[0]} — {new_row['Xep_loai'].iloc[0]}"
            )

df = st.session_state.df

# Hiển thị bảng dữ liệu (đầy đủ cột)
st.markdown("**📋 Bảng điểm sinh viên:**")
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ==================== 3. THỐNG KÊ MÔ TẢ ====================
st.subheader("3. Thống kê mô tả")

col1, col2, col3, col4 = st.columns(4)
col1.metric("📌 Tổng số SV", len(df))
col2.metric("📈 Điểm TB", f"{df['Tong_ket'].mean():.2f}")
col3.metric("🏆 Điểm cao nhất", f"{df['Tong_ket'].max():.2f}")
col4.metric("📉 Điểm thấp nhất", f"{df['Tong_ket'].min():.2f}")

st.markdown("**Số lượng sinh viên theo xếp loại:**")
thong_ke = df["Xep_loai"].value_counts().reindex(
    ["Giỏi", "Khá", "Trung bình", "Yếu"], fill_value=0
)
st.dataframe(
    thong_ke.rename_axis("Xếp loại").reset_index(name="Số lượng"),
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==================== 4. BIỂU ĐỒ ====================
st.subheader("4. Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(df["Họ và tên"], df["Tong_ket"], color="cornflowerblue")
ax.set_title("Điểm tổng kết của sinh viên")
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Tên sinh viên")
ax.set_xlim(0, 10)

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.divider()

# ==================== 5. TÌM KIẾM & LỌC ====================
st.subheader("5. Tìm kiếm và lọc sinh viên")

col_a, col_b = st.columns(2)
with col_a:
    tu_khoa = st.text_input("Nhập họ tên sinh viên")
with col_b:
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

st.write(f"🔎 Tìm thấy **{len(ket_qua)}** sinh viên:")
st.dataframe(ket_qua, use_container_width=True, hide_index=True)

st.divider()

# ==================== 6. TẢI FILE ====================
st.subheader("6. Tải bảng điểm")

col_csv, col_xlsx = st.columns(2)

with col_csv:
    csv_data = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Tải bảng điểm CSV",
        data=csv_data,
        file_name="bang_diem_sinh_vien.csv",
        mime="text/csv",
        use_container_width=True
    )

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

# ==================== 7. THÔNG TIN NGƯỜI TẠO ====================
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