import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Hệ thống Giám sát Lỗi Vận hành", layout="wide")

if 'db_errors' not in st.session_state:
    st.session_state.db_errors = pd.DataFrame(columns=['Ngày', 'Tháng', 'Cơ sở', 'Đối tượng', 'Tên nhân sự', 'Loại lỗi', 'Mức độ', 'Chi tiết'])

st.title("📊 DASHBOARD THEO DÕI LỖI VẬN HÀNH HỆ THỐNG")
st.markdown("---")

st.sidebar.header("🔐 PHÂN QUYỀN HỆ THỐNG")
role = st.sidebar.radio("Bạn là:", ["Khán giả (Sếp/Quản lý)", "Admin (Chủ sở hữu)"])

is_admin = False
if role == "Admin (Chủ sở hữu)":
    password = st.sidebar.text_input("Nhập mật khẩu Admin:", type="password")
    if password == "admin123":
        st.sidebar.success("Đăng nhập Admin thành công!")
        is_admin = True
    elif password != "":
        st.sidebar.error("Sai mật khẩu!")

if is_admin:
    st.subheader("📥 CẬP NHẬT DỮ LIỆU TỰ ĐỘNG (CHỈ ADMIN)")
    sheet_url = st.text_input("Dán đường dẫn Google Sheets công khai vào đây:")
    if sheet_url and st.button("🚀 BẮT ĐẦU ĐỌC FILE & CẬP NHẬT TỰ ĐỘNG"):
        with st.spinner("Đang cập nhật dữ liệu..."):
            try:
                if "edit?" in sheet_url:
                    csv_url = sheet_url.split("/edit")[0] + "/export?format=csv"
                    st.session_state.db_errors = pd.read_csv(csv_url)
                    st.success("🎉 Đã cập nhật thành công dữ liệu mới!")
            except Exception as e:
                st.error(f"Lỗi đọc file: {str(e)}")

if st.session_state.db_errors.empty:
    st.session_state.db_errors = pd.DataFrame([
        {'Ngày': '2026-06-20', 'Tháng': 'Tháng 6', 'Cơ sở': 'LONG BIÊN', 'Đối tượng': 'Nhân viên', 'Tên nhân sự': 'Nguyễn Văn A', 'Loại lỗi': 'Không chào khách', 'Mức độ': 'Nghiêm trọng - Cao', 'Chi tiết': 'Khách vào quầy không chào, bấm điện thoại'},
        {'Ngày': '2026-06-21', 'Tháng': 'Tháng 6', 'Cơ sở': 'TIME CITY', 'Đối tượng': 'CHT-CHP', 'Tên nhân sự': 'Quản lý Hùng', 'Loại lỗi': 'Nộp Sale muộn', 'Mức độ': 'Nghiêm trọng - Cao', 'Chi tiết': 'Nộp báo cáo doanh thu trễ 45 phút'}
    ])

df = st.session_state.db_errors
st.markdown("### 🔍 BỘ LỌC DỮ LIỆU")
col1, col2 = st.columns(2)
with col1:
    filter_month = st.multiselect("Chọn Tháng:", options=df['Tháng'].unique(), default=df['Tháng'].unique())
with col2:
    filter_branch = st.multiselect("Chọn Cơ sở:", options=df['Cơ sở'].unique(), default=df['Cơ sở'].unique())

filtered_df = df[(df['Tháng'].isin(filter_month)) & (df['Cơ sở'].isin(filter_branch))]

kpi1, kpi2 = st.columns(2)
with kpi1: st.metric(label="🚨 Tổng Số Lỗi Ghi Nhận", value=len(filtered_df))
with kpi2: st.metric(label="🏢 Số Cơ Sở Đang Lọc", value=len(filtered_df['Cơ sở'].unique()))

fig_bar = px.bar(filtered_df, x='Cơ sở', color='Mức độ', barmode='stack', title="Số lượng lỗi theo cơ sở")
st.plotly_chart(fig_bar, use_container_width=True)
st.dataframe(filtered_df, use_container_width=True)
