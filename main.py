# main.py
import streamlit as st
from db import fetch_all_nhan_vien, insert_nhan_vien

# Cấu hình trang (Luôn luôn là câu lệnh Streamlit hiển thị đầu tiên)
st.set_page_config(page_title="Quản lý Nhân sự", layout="wide")

st.title("HỆ THỐNG QUẢN LÝ THÔNG TIN NHÂN VIÊN")

# Chia giao diện làm 2 cột: Cột trái làm Form nhập liệu, Cột phải hiển thị danh sách
col_form, col_data = st.columns([1, 2])

with col_form:
    st.header("Thêm Nhân Viên Mới")

    # Sử dụng st.form để gom cụm tương tác, tránh hiện tượng tự động rerun khi đang gõ chữ
    with st.form("form_them_nhan_vien", clear_on_submit=True):
        ten_input = st.text_input("Họ và tên nhân viên:", placeholder="Nhập đầy đủ họ tên...")
        vi_tri_input = st.text_input("Vị trí công việc:", placeholder="Ví dụ: Kỹ sư phần mềm, Kế toán...")
        don_vi_input = st.text_input("Đơn vị / Phòng ban:", placeholder="Ví dụ: Phòng IT, Phòng Nhân sự...")

        # Nút submit của form
        submit_button = st.form_submit_button("Lưu vào Hệ thống")

    if submit_button:
        # ---- BƯỚC 1: VALIDATION (KIỂM TRA DỮ LIỆU) ----
        if not ten_input.strip():
            st.error("Lỗi: Không được để trống Họ và tên nhân viên!")
        elif not vi_tri_input.strip():
            st.error("Lỗi: Không được để trống Vị trí công việc!")
        elif not don_vi_input.strip():
            st.error("Lỗi: Không được để trống Đơn vị / Phòng ban!")
        else:
            # ---- BƯỚC 2: THỰC THI LƯU DỮ LIỆU ----
            success = insert_nhan_vien(
                ten_input.strip(), vi_tri_input.strip(), don_vi_input.strip()
            )
            if success:
                st.success(f"Thành công: Đã thêm nhân viên '{ten_input}' vào SQL!")
                # Kích hoạt làm mới giao diện ngay lập tức để đồng bộ dữ liệu mới lên bảng
                st.session_state.message = 'Thêm thành công'
                st.rerun()
            else:
                st.error("Thất bại: Hệ thống lỗi hoặc mất kết nối cơ sở dữ liệu.")

with col_data:
    st.header("Danh Sách Nhân Viên Hiện Tại")

    # Tải dữ liệu thật từ hàm SELECT
    df_nhan_vien = fetch_all_nhan_vien()

    if df_nhan_vien.empty:
        st.info("Hiện tại chưa có dữ liệu nhân viên nào trong hệ thống hoặc lỗi kết nối DB.")
    else:
        # Hiển thị bảng tương tác, tự động co giãn theo chiều rộng trang
        st.dataframe(df_nhan_vien, use_container_width=True)
if "action" not in st.session_state:
    st.session_state['action'] ='view'
# 2. Tạo nút nhấn để chuyển đổi qua lại giữa 'view' và 'insert'
if st.button("Chuyển đổi Chế độ (View / Insert)"):
    if st.session_state['action'] == "view":
        st.session_state['action'] = "insert"
    else:
        st.session_state['action'] = "view"
    
    # Rerun để Streamlit cập nhật lại giao diện ngay lập tức
    st.rerun()

# 3. Hiển thị giá trị hiện tại ra màn hình
st.write(f"Chế độ hiện tại: **{st.session_state['action']}**")