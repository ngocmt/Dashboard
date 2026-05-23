# db.py
import mysql.connector
import pandas as pd
from config import DB_CONFIG


def get_connection():
    """Khởi tạo kết nối đến MySQL với try-except"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
        return None


def fetch_all_nhan_vien():
    """Đọc toàn bộ danh sách nhân viên trả về dưới dạng Pandas DataFrame"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()

    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, ten AS 'Họ và Tên', vi_tri AS 'Vị trí', don_vi AS 'Đơn vị', ngay_tao AS 'Ngày tạo' FROM nhan_vien ORDER BY id DESC"

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return pd.DataFrame(result)
    except mysql.connector.Error as e:
        print(f"Lỗi truy vấn SELECT: {e}")
        return pd.DataFrame()
    finally:
        cursor.close()
        conn.close()


def insert_nhan_vien(ten, vi_tri, don_vi):
    """Thêm nhân viên mới sử dụng Parameterized Query để chống SQL Injection"""
    conn = get_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    # Sử dụng %s làm placeholder an toàn
    query = "INSERT INTO nhan_vien (ten, vi_tri, don_vi) VALUES (%s, %s, %s)"
    values = (ten, vi_tri, don_vi)

    try:
        cursor.execute(query, values)
        conn.commit()  # BẮT BUỘC: Lưu lại các thay đổi vào MySQL
        return True
    except mysql.connector.Error as e:
        print(f"Lỗi truy vấn INSERT: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        # In ra màn hình terminal để debug thay vì treo ứng dụng
        print(f"Lỗi kết nối rồi: {e}")
        return None
