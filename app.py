import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(page_title="Hệ thống Dashboard Giám Sát Lỗi Mới", layout="wide")

# Khởi tạo cơ sở dữ liệu ảo theo Form 9 cột mới nếu chưa có dữ liệu đầu vào
if 'db_errors_v2' not in st.session_state:
    st.session_state.db_errors_v2 = pd.DataFrame(columns=[
        'Ngày tháng', 'Cơ sở', 'Gian hàng', 'Tên nhân sự vi phạm', 'Chức vụ', 
        'Mô tả chi tiết lỗi từ Came or lỗi từ cơ sở', 'Tính chất nghiêm trọng', 'Mức chế tài', 'Phương án cải thiện'
    ])

# 2. GIAO DIỆN TIÊU ĐỀ CHÍNH
st.title("📊 Dashboard Giám Sát & Quản Lý Lỗi Vận Hành (Bản Mới V2)")
st.markdown("---")

# 3. PHÂN QUYỀN ADMIN ĐỂ CẬP NHẬT GOOGLE SHEETS
st.sidebar.header("🔐 QUẢN TRỊ VIÊN")
role = st.sidebar.radio("Bạn là:", ["Xem Báo Cáo", "Admin (Cập nhật dữ liệu)"])

is_admin = False
if role == "Admin (Cập nhật dữ liệu)":
    password = st.sidebar.text_input("Mật khẩu kết nối:", type="password")
    if password == "admin123":
        st.sidebar.success("Mở khóa quyền cập nhật thành công!")
        is_admin = True
    elif password != "":
        st.sidebar.error("Sai mật khẩu!")

if is_admin:
    st.subheader("📥 ĐỒNG BỘ DỮ LIỆU TỪ GOOGLE SHEETS FORM MỚI")
    sheet_url = st.text_input("Dán đường dẫn link Google Sheets (Form 9 cột) của bạn:")
    if sheet_url and st.button("🚀 CẬP NHẬT LÊN DASHBOARD"):
        with st.spinner("Đang xử lý đồng bộ dữ liệu biểu đồ..."):
            try:
                if "edit?" in sheet_url:
                    csv_url = sheet_url.split("/edit")[0] + "/export?format=csv"
                    st.session_state.db_errors_v2 = pd.read_csv(csv_url)
                    st.success("🎉 Đã đồng bộ thành công dữ liệu Form mới lên biểu đồ!")
            except Exception as e:
                st.error(f"Lỗi đọc dữ liệu: {str(e)}. Hãy chắc chắn các tên cột trên Google Sheet trùng khớp 100% với form mới.")

# Nếu chưa có dữ liệu, tự động kích hoạt dữ liệu mẫu chuẩn form mới để hiển thị biểu đồ đẹp mắt
if st.session_state.db_errors_v2.empty:
    sample_data = [
        {'Ngày tháng': '2026-06-20', 'Cơ sở': 'LONG BIÊN', 'Gian hàng': 'Quầy Thu Ngân', 'Tên nhân sự vi phạm': 'Nguyễn Văn A', 'Chức vụ': 'Nhân viên', 'Mô tả chi tiết lỗi từ Came or lỗi từ cơ sở': 'Không chào khách, đưa tiền bằng 1 tay.', 'Tính chất nghiêm trọng': 'Nghiêm trọng - Cao', 'Mức chế tài': 'Trừ 20 điểm KPI', 'Phương án cải thiện': 'Training lại bộ quy chuẩn giao tiếp.'},
        {'Ngày tháng': '2026-06-21', 'Cơ sở': 'TIME CITY', 'Gian hàng': 'Khu Trò Chơi', 'Tên nhân sự vi phạm': 'Trần Thị B', 'Chức vụ': 'CHT-CHP', 'Mô tả chi tiết lỗi từ Came or lỗi từ cơ sở': 'Nộp Sale muộn, sai lệch bảng DK-TT.', 'Tính chất nghiêm trọng': 'Nghiêm trọng - Cao', 'Mức chế tài': 'Phạt 100,000đ', 'Phương án cải thiện': 'Setup chuông báo thức nhắc việc.'},
        {'Ngày tháng': '2026-06-22', 'Cơ sở': 'HẢI PHÒNG', 'Gian hàng': 'Khu Farm/Thú', 'Tên nhân sự vi phạm': 'Lê Văn C', 'Chức vụ': 'Nhân viên', 'Mô tả chi tiết lỗi từ Came or lỗi từ cơ sở': 'Bình tương cà lem dính bẩn đầu ca.', 'Tính chất nghiêm trọng': 'Thấp', 'Mức chế tài': 'Nhắc nhở nội bộ', 'Phương án cải thiện': 'Kiểm tra checklist bàn giao ca.'},
        {'Ngày tháng': '2026-06-23', 'Cơ sở': 'ROYAL CITY', 'Gian hàng': 'Quầy Thu Ngân', 'Tên nhân sự vi phạm': 'Phạm Minh D', 'Chức vụ': 'Nhân viên', 'Mô tả chi tiết lỗi từ Came or lỗi từ cơ sở': 'Sử dụng điện thoại liên tục lướt mạng.', 'Tính chất nghiêm trọng': 'Nghiêm trọng - Cao', 'Mức chế tài': 'Trừ 20 điểm KPI', 'Phương án cải thiện': 'Tịch thu điện thoại đầu ca.'},
        {'Ngày tháng': '2026-06-24', 'Cơ sở': 'LOTTE TÂY HỒ', 'Gian hàng': 'Khu Nhà Banh', 'Tên nhân sự vi phạm': 'Hoàng Thị E', 'Chức vụ': 'Nhân viên', 'Mô tả chi tiết lỗi từ Came or lỗi từ cơ sở': 'Tụ tập nói chuyện riêng, lơ là khách.', 'Tính chất nghiêm trọng': 'Trung bình', 'Mức chế tài': 'Phạt 50,000đ', 'Phương án cải thiện': 'Điều phối lại vị trí đứng cụ thể.'}
    ]
    st.session_state.db_errors_v2 = pd.DataFrame(sample_data)

df = st.session_state.db_errors_v2

# 4. THANH BỘ LỌC THÔNG MINH THEO CẤU TRÚC MỚI
st.markdown("### 🔍 BỘ LỌC DỮ LIỆU ĐA NĂNG")
f_col1, f_col2, f_col3 = st.columns(3)
with f_col1:
    filter_branch = st.multiselect("Lọc theo Cơ sở:", options=sorted(df['Cơ sở'].unique()), default=df['Cơ sở'].unique())
with f_col2:
    filter_booth = st.multiselect("Lọc theo Gian hàng:", options=sorted(df['Gian hàng'].unique()), default=df['Gian hàng'].unique())
with f_col3:
    filter_severity = st.multiselect("Lọc Tính chất nghiêm trọng:", options=df['Tính chất nghiêm trọng'].unique(), default=df['Tính chất nghiêm trọng'].unique())

# Áp dụng bộ lọc vào bảng dữ liệu
filtered_df = df[
    (df['Cơ sở'].isin(filter_branch)) & 
    (df['Gian hàng'].isin(filter_booth)) & 
    (df['Tính chất nghiêm trọng'].isin(filter_severity))
]

# 5. KHU VỰC THỂ HIỆN BIỂU ĐỒ PHÂN TÍCH (CHART AREA)
st.markdown("---")
st.markdown("### 📈 BIỂU ĐỒ PHÂN TÍCH THÔNG MINH")

chart_col1, chart_col2 = st.columns([2, 1])

with chart_col1:
    st.write("**📊 Biểu đồ số lượng lỗi theo từng Cơ sở (Phân tách mức độ)**")
    if not filtered_df.empty:
        fig_bar = px.bar(
            filtered_df, x='Cơ sở', color='Tính chất nghiêm trọng',
            barmode='stack', text_auto=True,
            color_discrete_map={'Nghiêm trọng - Cao': '#EF553B', 'Trung bình': '#FECB52', 'Thấp': '#636EFA'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Không có dữ liệu thỏa mãn bộ lọc để vẽ biểu đồ cột.")

with chart_col2:
    st.write("**🍩 Tỷ lệ phân bổ tính chất nghiêm trọng**")
    if not filtered_df.empty:
        fig_pie = px.pie(
            filtered_df, names='Tính chất nghiêm trọng', hole=0.4,
            color='Tính chất nghiêm trọng',
            color_discrete_map={'Nghiêm trọng - Cao': '#EF553B', 'Trung bình': '#FECB52', 'Thấp': '#636EFA'}
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Không có dữ liệu vẽ biểu đồ tròn.")

# BIỂU ĐỒ THỨ 3: LỖI PHÂN BỔ THEO GIAN HÀNG
st.write("**🏪 Biểu đồ mật độ lỗi xuất hiện tại các Gian hàng**")
if not filtered_df.empty:
    fig_booth = px.histogram(
        filtered_df, x='Gian hàng', color='Chức vụ', 
        barmode='group', text_auto=True,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_booth, use_container_width=True)

# 6. BẢNG CHI TIẾT ĐẦY ĐỦ 9 CỘT MỚI
st.markdown("### 📋 DANH SÁCH CHI TIẾT LỖI VI PHẠM (FORM MỚI)")
st.dataframe(filtered_df, use_container_width=True)
