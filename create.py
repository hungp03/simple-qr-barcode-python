# -*- coding: utf-8 -*-
from tkinter import messagebox
import qrcode
import barcode
from datetime import datetime
from PIL import Image, ImageTk
import os
from barcode.writer import ImageWriter
from unidecode import unidecode
from barcode import Code128

# hàm trả về chuỗi tạo tên QR
def generate_filename():
    # Lấy thời gian hiện tại
    now = datetime.now()
    # Định dạng chuỗi theo yyyMMddHHmmss
    timestamp = now.strftime("%Y%m%d%H%M%S")
    # Kết hợp với phần mở rộng của tệp ảnh
    filename = f"{timestamp}.png"
    
    return filename

# version: phiên bản qr, phiên bản càng cao càng chứa nhiều dữ liệu
# error_correction: Khả năng sửa lỗi
# box_size: Kích thước của mỗi ô vuông trong mã QR
# border: Kích thước của viền (border) xung quanh mã QR

def generate_qr_code(text):
    # Chuyển đổi dữ liệu thành chuỗi UTF-8
    utf8_text = text.encode('utf-8')
    
    qr = qrcode.QRCode(version=10, error_correction=qrcode.ERROR_CORRECT_H, box_size=5, border=5)
    # Thêm dữ liệu vào mã QR (sử dụng dữ liệu đã mã hóa UTF-8)
    qr.add_data(utf8_text)
    # Tham số fit=True đảm bảo rằng mã QR sẽ tràn viền ảnh
    qr.make(fit=True)
    # Tạo ảnh từ mã QR đã tạo
    # Màu nền là trắng ("white"), fill là đen ("black")
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def save_qr_code(img):
    filename = "qrcode-" + generate_filename()
    img.save(filename)
    return filename


def show_qr_code(entry_text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(entry_text)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    path =  save_qr_code(img)
    messagebox.showinfo("Saved", f"QRcode lưu tại: {path}.")
    return path


# Hàm tạo mã barcode
def generate_barcode(entry_text):
    try:
        barcode_class = barcode.get_barcode_class('code128')
        barcode_instance = barcode_class(entry_text, writer=ImageWriter())
        img = barcode_instance.render()
        return img
    except ValueError as e:
        messagebox.showerror("Error", str(e))

    
# Hàm lưu mã barcode
def save_barcode(barcode_img):
    filename = "barcode-" + generate_filename()
    barcode_img.save(filename)
    return filename

# Hàm hiển thị mã barcode
def show_barcode(entry_text):
    txt = unidecode(entry_text)
    if txt != entry_text:
        messagebox.showerror("Lỗi", "Barcode chỉ chấp nhận số và chữ thông thường")
        return
    CODE128 = barcode.get_barcode_class('code128')
    code128 = CODE128(entry_text, writer=ImageWriter())
    img = generate_barcode(entry_text)
    path = save_barcode(img)
    messagebox.showinfo("Saved", f"Barcode lưu tại: {path}.")
    return path


