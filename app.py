import streamlit as st
import pandas as pd
import plotly.express as px
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
# 1. CẤU HÌNH TRANG WEB
st.set_page_config(page_title="Dashboard Giám Sát Lỗi Camera V2", layout="wide")

# Thiết lập tiêu đề giao diện
st.title("📊 Dashboard Giám Sát Lỗi Vận Hành & Camera (Form Mới)")
st.markdown("---")

# Khởi tạo dữ liệu ảo cấu trúc 9 cột mới đề phòng Google Sheet trống hoặc chưa đồng bộ
if 'db_v2' not in st.session_state:
    st.session_state.db_v2 = pd.DataFrame(columns=[
        'Ngày tháng', 'Cơ sở', 'Gian hàng', 'Tên nhân sự vi phạm', 'Chức vụ', 
        'Mô tả chi tiết lỗi từ Came or lỗi từ cơ sở', 'Tính chất nghiêm trọng', 'Mức chế tài', 'Phương án cải thiện'
    ])

# 2. KHU VỰC CẤU HÌNH ĐỒNG BỘ GOOGLE SHEET
st.sidebar.header("🔐 KẾT NỐI DỮ LIỆU")
sheet_url = st.sidebar.text_input("Dán link Google Sheets của bạn tại đây:")

if sheet_url:
    with st.spinner("Đang đồng bộ dữ liệu với Google Sheet..."):
        try:
            if "edit?" in sheet_url:
                csv_url = sheet_url.split("/edit")[0] + "/export?format=csv"
                # Đọc dữ liệu trực tiếp và xóa các dòng trống nếu có
                downloaded_df = pd.read_csv(csv_url).dropna(how='all')
                
                # Chuẩn hóa tên cột (bỏ khoảng trắng thừa)
                downloaded_df.columns = downloaded_df.columns.str.strip()
                st.session_state.db_v2 = downloaded_df
                st.sidebar.success("🎉 Đồng bộ dữ liệu thành công!")
        except Exception as e:
            st.sidebar.error(f"Lỗi đọc dữ liệu: {str(e)}. Vui lòng kiểm tra lại quyền chia sẻ link.")

# Gán dữ liệu làm việc chính
df = st.session_state.db_v2

# Trường hợp dữ liệu trống, hiển thị mẫu để người dùng dễ hình dung biểu đồ
if df.empty:
    sample_data = [
        {'Ngày tháng': '2026-06-20', 'Cơ sở': 'LONG BIÊN', 'Gian hàng': 'Quầy Thu Ngân', 'Tên nhân sự vi phạm': 'Nguyễn Văn A', 'Chức vụ': 'Nhân viên', 'Mô tả chi tiết lỗi từ Came or lỗi từ cơ sở': 'Không chào khách khi giao dịch.', 'Tính chất nghiêm trọng': 'Nghiêm trọng - Cao', 'Mức chế tài': 'Trừ 20 điểm KPI', 'Phương án cải thiện': 'Training lại bộ quy chuẩn giao tiếp.'},
        {'Ngày tháng': '2026-06-21', 'Cơ sở': 'TIME CITY', 'Gian hàng': 'Khu Trò Chơi', 'Tên nhân sự vi phạm': 'Trần Thị B', 'Chức vụ': 'CHT-CHP', 'Mô tả chi tiết lỗi từ Came or lỗi từ cơ sở': 'Nộp báo cáo doanh thu muộn.', 'Tính chất nghiêm trọng': 'Trung bình', 'Mức chế tài': 'Phạt 100,000đ', 'Phương án cải thiện': 'Setup báo thức lịch làm việc.'}
    ]
    df = pd.DataFrame(sample_data)

# Kiểm tra đảm bảo các cột cần thiết tồn tại trước khi xử lý bộ lọc và biểu đồ
required_cols = ['Cơ sở', 'Gian hàng', 'Tính chất nghiêm trọng']
if all(col in df.columns for col in required_cols):
    
    # 3. BỘ LỌC DỮ LIỆU THÔNG MINH
    st.markdown("### 🔍 BỘ LỌC DỮ LIỆU")
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        filter_branch = st.multiselect("Lọc theo Cơ sở:", options=sorted(df['Cơ sở'].unique()), default=df['Cơ sở'].unique())
    with f_col2:
        filter_booth = st.multiselect("Lọc theo Gian hàng:", options=sorted(df['Gian hàng'].unique()), default=df['Gian hàng'].unique())
    with f_col3:
        filter_severity = st.multiselect("Lọc Tính chất nghiêm trọng:", options=df['Tính chất nghiêm trọng'].unique(), default=df['Tính chất nghiêm trọng'].unique())

    # Áp dụng bộ lọc
    filtered_df = df[
        (df['Cơ sở'].isin(filter_branch)) & 
        (df['Gian hàng'].isin(filter_booth)) & 
        (df['Tính chất nghiêm trọng'].isin(filter_severity))
    ]

    # 4. HỆ THỐNG BIỂU ĐỒ PHÂN TÍCH THÔNG MINH
    st.markdown("---")
    st.markdown("### 📈 BIỂU ĐỒ PHÂN TÍCH")

    chart_col1, chart_col2 = st.columns([2, 1])

    with chart_col1:
        st.write("**📊 Tổng hợp số lượng lỗi theo từng Cơ sở**")
        if not filtered_df.empty:
            fig_bar = px.bar(
                filtered_df, x='Cơ sở', color='Tính chất nghiêm trọng',
                barmode='stack', text_auto=True,
                color_discrete_map={'Nghiêm trọng - Cao': '#EF553B', 'Trung bình': '#FECB52', 'Thấp': '#636EFA'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Không có dữ liệu phù hợp bộ lọc.")

    with chart_col2:
        st.write("**🍩 Tỷ lệ mức độ nghiêm trọng**")
        if not filtered_df.empty:
            fig_pie = px.pie(
                filtered_df, names='Tính chất nghiêm trọng', hole=0.4,
                color='Tính chất nghiêm trọng',
                color_discrete_map={'Nghiêm trọng - Cao': '#EF553B', 'Trung bình': '#FECB52', 'Thấp': '#636EFA'}
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # Biểu đồ lỗi theo Gian hàng
    st.write("**🏪 Tình hình vi phạm phân bổ theo các Gian hàng**")
    if not filtered_df.empty:
        fig_booth = px.histogram(
            filtered_df, x='Gian hàng', color='Chức vụ',
            barmode='group', text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig_booth, use_container_width=True)

    # 5. BẢNG DỮ LIỆU CHI TIẾT
    st.markdown("---")
    st.markdown("### 📋 DANH SÁCH CHI TIẾT LỖI VI PHẠM")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.error("⚠️ Lỗi cấu trúc: File Google Sheets của bạn không khớp các tiêu đề cột form mới. Vui lòng đảm bảo các cột đầu tiên được đặt tên chính xác là: 'Ngày tháng', 'Cơ sở', 'Gian hàng', 'Tên nhân sự vi phạm', 'Chức vụ', 'Mô tả chi tiết lỗi từ Came or lỗi từ cơ sở', 'Tính chất nghiêm trọng', 'Mức chế tài', 'Phương án cải thiện'.")
