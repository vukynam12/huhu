# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# ==================== CẤU HÌNH TRANG ====================
st.set_page_config(
    page_title="Student Score Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS TÙY CHỈNH ====================
st.markdown("""
<style>
    /* Font & background */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Roboto', sans-serif;
    }

    /* Header gradient */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 700;
    }
    .main-header p {
        margin: 6px 0 0 0;
        opacity: 0.9;
        font-size: 15px;
    }

    /* KPI Cards */
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
    }
    .kpi-label {
        font-size: 13px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #2c3e50;
    }
    .kpi-blue   { border-left-color: #667eea; }
    .kpi-green  { border-left-color: #38b2ac; }
    .kpi-orange { border-left-color: #ed8936; }
    .kpi-red    { border-left-color: #f56565; }

    /* Section header */
    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #2c3e50;
        margin: 10px 0 15px 0;
        padding-left: 12px;
        border-left: 4px solid #667eea;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #aaa;
        font-size: 12px;
        padding: 20px 0;
        margin-top: 30px;
        border-top: 1px solid #eee;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9ff 0%, #eef0ff 100%);
    }
</style>
""", unsafe_allow_html=True)

# ==================== HÀM TÍNH ĐIỂM ====================
def tinh_tong_ket(row):
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
    d = pd.DataFrame(raw)
    d["Tong_ket"] = d.apply(tinh_tong_ket, axis=1)
    d["Xep_loai"] = d["Tong_ket"].apply(xep_loai)
    return d

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## 🎓 Score Dashboard")
    st.markdown("---")

    menu = st.radio(
        "📌 **Chức năng**",
        [
            "🏠 Tổng quan",
            "📥 Nhập dữ liệu",
            "📊 Biểu đồ",
            "🔍 Tìm kiếm & Lọc",
            "💾 Tải xuống",
            "ℹ️ Giới thiệu"
        ]
    )

    st.markdown("---")
    st.markdown("### ⚙️ Cài đặt")
    trong_so_cc = st.slider("Trọng số Chuyên cần (%)", 0, 50, 10, 5)
    trong_so_gk = st.slider("Trọng số Giữa kì (%)",   0, 50, 30, 5)
    trong_so_ck = 100 - trong_so_cc - trong_so_gk
    st.caption(f"→ Cuối kì: **{trong_so_ck}%**")

    st.markdown("---")
    st.caption("👩‍💻 **Phùng Thanh Mai**")
    st.caption("MSSV: 026308010392")

# ==================== TÍNH LẠI ĐIỂM THEO TRỌNG SỐ MỚI ====================
def tinh_lai(df, w_cc, w_gk, w_ck):
    d = df.copy()
    d["Tong_ket"] = (
        w_cc/100 * d["Điểm chuyên cần"]
        + w_gk/100 * d["Điểm giữa kì"]
        + w_ck/100 * d["Điểm cuối kì"]
    ).round(2)
    d["Xep_loai"] = d["Tong_ket"].apply(xep_loai)
    return d

# Khởi tạo session
if "df" not in st.session_state:
    st.session_state.df = build_df(DEFAULT_DATA)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 Student Score Dashboard</h1>
    <p>Quản lý – Phân tích – Trực quan hóa điểm sinh viên</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
#  🏠 TỔNG QUAN
# ==================================================
if menu == "🏠 Tổng quan":
    df = tinh_lai(st.session_state.df, trong_so_cc, trong_so_gk, trong_so_ck)

    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card kpi-blue">
            <div class="kpi-label">Tổng sinh viên</div>
            <div class="kpi-value">{len(df)}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card kpi-green">
            <div class="kpi-label">Điểm trung bình</div>
            <div class="kpi-value">{df['Tong_ket'].mean():.2f}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card kpi-orange">
            <div class="kpi-label">Điểm cao nhất</div>
            <div class="kpi-value">{df['Tong_ket'].max():.2f}</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card kpi-red">
            <div class="kpi-label">Điểm thấp nhất</div>
            <div class="kpi-value">{df['Tong_ket'].min():.2f}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2 cột: bảng dữ liệu + biểu đồ tròn
    col_table, col_pie = st.columns([2, 1])

    with col_table:
        st.markdown('<div class="section-title">📋 Bảng điểm sinh viên</div>',
                    unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True, height=420)

    with col_pie:
        st.markdown('<div class="section-title">🥧 Tỷ lệ xếp loại</div>',
                    unsafe_allow_html=True)
        counts = df["Xep_loai"].value_counts().reindex(
            ["Giỏi", "Khá", "Trung bình", "Yếu"], fill_value=0
        )
        fig, ax = plt.subplots(figsize=(4, 4))
        colors = ["#667eea", "#38b2ac", "#ed8936", "#f56565"]
        wedges, _, autotexts = ax.pie(
            counts, labels=counts.index, autopct="%1.0f%%",
            colors=colors, startangle=90,
            wedgeprops={"edgecolor": "white", "linewidth": 2}
        )
        for t in autotexts:
            t.set_color("white")
            t.set_fontweight("bold")
        ax.set_title("")
        st.pyplot(fig)
        plt.close(fig)

# ==================================================
#  📥 NHẬP DỮ LIỆU
# ==================================================
elif menu == "📥 Nhập dữ liệu":
    st.markdown('<div class="section-title">📥 Nhập dữ liệu sinh viên</div>',
                unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🎯 Dữ liệu mẫu", "📁 Tải CSV", "✍️ Nhập tay"])

    with tab1:
        st.info("Nhấn nút bên dưới để **reset** về bộ dữ liệu mẫu gồm 10 sinh viên.")
        if st.button("🔄 Dùng dữ liệu mẫu", use_container_width=True):
            st.session_state.df = build_df(DEFAULT_DATA)
            st.success("✅ Đã khôi phục dữ liệu mẫu!")
            st.rerun()

    with tab2:
        uploaded_file = st.file_uploader(
            "Chọn file CSV (cần cột: 'Họ và tên', 'Điểm chuyên cần', 'Điểm giữa kì', 'Điểm cuối kì')",
            type=["csv"]
        )
        if uploaded_file is not None:
            try:
                df_upload = pd.read_csv(uploaded_file)
                required = {"Họ và tên", "Điểm chuyên cần",
                            "Điểm giữa kì", "Điểm cuối kì"}
                if required.issubset(df_upload.columns):
                    st.session_state.df = build_df(df_upload.to_dict("list"))
                    st.success(f"✅ Đã tải {len(df_upload)} sinh viên!")
                else:
                    st.error(f"❌ File thiếu cột. Cần: {required}")
            except Exception as e:
                st.error(f"❌ Lỗi đọc file: {e}")

    with tab3:
        with st.form("form_nhap", clear_on_submit=True):
            st.write("**Thêm sinh viên mới:**")
            ho_ten = st.text_input("Họ và tên")
            c1, c2, c3 = st.columns(3)
            with c1:
                cc = st.number_input("Điểm chuyên cần", 0.0, 10.0, 8.0, 0.5)
            with c2:
                gk = st.number_input("Điểm giữa kì", 0.0, 10.0, 7.0, 0.5)
            with c3:
                ck = st.number_input("Điểm cuối kì", 0.0, 10.0, 7.0, 0.5)
            submitted = st.form_submit_button("➕ Thêm sinh viên",
                                              use_container_width=True)

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
                st.success(f"✅ Đã thêm: **{ho_ten}** — {new_row['Tong_ket'].iloc[0]} điểm")
                st.rerun()

    st.markdown("---")
    st.markdown("**📋 Dữ liệu hiện tại:**")
    st.dataframe(st.session_state.df, use_container_width=True, hide_index=True)

# ==================================================
#  📊 BIỂU ĐỒ
# ==================================================
elif menu == "📊 Biểu đồ":
    df = tinh_lai(st.session_state.df, trong_so_cc, trong_so_gk, trong_so_ck)

    st.markdown('<div class="section-title">📊 Trực quan hóa điểm</div>',
                unsafe_allow_html=True)

    loai_bieu_do = st.selectbox(
        "Chọn loại biểu đồ:",
        ["Cột ngang (Bar)", "Cột dọc (Column)",
         "So sánh 3 điểm thành phần", "Đường (Line)"]
    )

    fig, ax = plt.subplots(figsize=(11, 6))

    if loai_bieu_do == "Cột ngang (Bar)":
        colors = ["#667eea" if d >= 8 else "#38b2ac" if d >= 6.5
                  else "#ed8936" if d >= 5 else "#f56565"
                  for d in df["Tong_ket"]]
        ax.barh(df["Họ và tên"], df["Tong_ket"], color=colors)
        ax.set_xlabel("Điểm tổng kết", fontsize=12)
        ax.set_xlim(0, 10)
        for i, v in enumerate(df["Tong_ket"]):
            ax.text(v + 0.1, i, f"{v}", va="center", fontweight="bold")

    elif loai_bieu_do == "Cột dọc (Column)":
        colors = ["#667eea" if d >= 8 else "#38b2ac" if d >= 6.5
                  else "#ed8936" if d >= 5 else "#f56565"
                  for d in df["Tong_ket"]]
        ax.bar(range(len(df)), df["Tong_ket"], color=colors)
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels(df["Họ và tên"], rotation=30, ha="right")
        ax.set_ylabel("Điểm tổng kết", fontsize=12)
        ax.set_ylim(0, 10)
        for i, v in enumerate(df["Tong_ket"]):
            ax.text(i, v + 0.15, f"{v}", ha="center", fontweight="bold")

    elif loai_bieu_do == "So sánh 3 điểm thành phần":
        x = range(len(df))
        w = 0.27
        ax.bar([i - w for i in x], df["Điểm chuyên cần"], w,
               label="Chuyên cần", color="#667eea")
        ax.bar(x, df["Điểm giữa kì"], w,
               label="Giữa kì", color="#38b2ac")
        ax.bar([i + w for i in x], df["Điểm cuối kì"], w,
               label="Cuối kì", color="#ed8936")
        ax.set_xticks(list(x))
        ax.set_xticklabels(df["Họ và tên"], rotation=30, ha="right")
        ax.set_ylim(0, 11)
        ax.legend(loc="upper right")
        ax.set_ylabel("Điểm", fontsize=12)

    else:  # Line
        ax.plot(df["Họ và tên"], df["Tong_ket"],
                marker="o", color="#667eea", linewidth=2.5, markersize=8)
        ax.set_xticklabels(df["Họ và tên"], rotation=30, ha="right")
        ax.set_ylim(0, 10)
        ax.grid(True, alpha=0.3)
        ax.set_ylabel("Điểm tổng kết", fontsize=12)

    ax.set_title("Biểu đồ điểm sinh viên", fontsize=14, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ==================================================
#  🔍 TÌM KIẾM & LỌC
# ==================================================
elif menu == "🔍 Tìm kiếm & Lọc":
    df = tinh_lai(st.session_state.df, trong_so_cc, trong_so_gk, trong_so_ck)

    st.markdown('<div class="section-title">🔍 Tìm kiếm và lọc sinh viên</div>',
                unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        tu_khoa = st.text_input("🔎 Nhập họ tên sinh viên")
    with col_b:
        loai = st.selectbox("🏅 Xếp loại",
                            ["Tất cả", "Giỏi", "Khá", "Trung bình", "Yếu"])
    with col_c:
        diem_min = st.number_input("Điểm tối thiểu", 0.0, 10.0, 0.0, 0.5)

    ket_qua = df.copy()
    if tu_khoa.strip():
        ket_qua = ket_qua[ket_qua["Họ và tên"].str.contains(
            tu_khoa, case=False, na=False)]
    if loai != "Tất cả":
        ket_qua = ket_qua[ket_qua["Xep_loai"] == loai]
    if diem_min > 0:
        ket_qua = ket_qua[ket_qua["Tong_ket"] >= diem_min]

    st.success(f"🔎 Tìm thấy **{len(ket_qua)}** sinh viên phù hợp.")
    st.dataframe(ket_qua, use_container_width=True, hide_index=True)

# ==================================================
#  💾 TẢI XUỐNG
# ==================================================
elif menu == "💾 Tải xuống":
    df = tinh_lai(st.session_state.df, trong_so_cc, trong_so_gk, trong_so_ck)

    st.markdown('<div class="section-title">💾 Tải bảng điểm về máy</div>',
                unsafe_allow_html=True)

    st.info(f"📋 Bảng điểm hiện có **{len(df)}** sinh viên. Chọn định dạng để tải xuống:")

    col_csv, col_xlsx = st.columns(2)

    with col_csv:
        csv_data = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "⬇️ Tải file CSV",
            data=csv_data,
            file_name="bang_diem_sinh_vien.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )

    with col_xlsx:
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Bang diem")
        st.download_button(
            "⬇️ Tải file Excel",
            data=excel_buffer.getvalue(),
            file_name="bang_diem_sinh_vien.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary"
        )

    st.markdown("---")
    st.markdown("**Xem trước dữ liệu sẽ tải:**")
    st.dataframe(df, use_container_width=True, hide_index=True)

# ==================================================
#  ℹ️ GIỚI THIỆU
# ==================================================
else:
    st.markdown('<div class="section-title">ℹ️ Giới thiệu ứng dụng</div>',
                unsafe_allow_html=True)

    st.markdown("""
    ### 🎓 Student Score Dashboard

    Ứng dụng hỗ trợ **quản lý – phân tích – trực quan hóa** điểm sinh viên.

    #### ✨ Tính năng chính
    | # | Chức năng | Mô tả |
    |---|---|---|
    | 1 | 📥 Nhập dữ liệu | Dữ liệu mẫu / Upload CSV / Nhập tay |
    | 2 | 🏠 Tổng quan | KPI cards + bảng điểm + biểu đồ tròn |
    | 3 | 📊 Biểu đồ | 4 loại: Bar, Column, So sánh, Line |
    | 4 | 🔍 Tìm kiếm & Lọc | Theo tên, xếp loại, điểm tối thiểu |
    | 5 | 💾 Tải xuống | Xuất CSV / Excel |

    #### 📐 Công thức tính điểm
    Điểm tổng kết = **W₁ × Chuyên cần + W₂ × Giữa kì + W₃ × Cuối kì**

    > Trọng số mặc định: **10% / 30% / 60%** — có thể tùy chỉnh ở **sidebar bên trái**.

    #### 🏅 Xếp loại
    - **Giỏi**: ≥ 8.0
    - **Khá**: 6.5 – 7.9
    - **Trung bình**: 5.0 – 6.4
    - **Yếu**: < 5.0
    """)

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    💻 Phát triển bởi <b>Phùng Thanh Mai</b> · MSSV: 026308010392<br>
    © 2024 · Student Score Dashboard
</div>
""", unsafe_allow_html=True)