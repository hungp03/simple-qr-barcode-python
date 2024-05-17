# -*- coding: utf-8 -*-
from tkinter import messagebox, filedialog
import pyperclip
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import os

def scan_option():
        response = messagebox.askquestion("Scan", "Bạn muốn quét QR từ ảnh trong máy tính?\nChọn Yes để scan từ camera, No để lấy ảnh trong máy")
        if response == 'yes':
            scan_from_camera()
        else:
            open_file()
            

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        decode_image(file_path)

def decode_image(path):
    try:
        fo = open("readqr.txt", 'a', encoding='utf-8')
        absolute_path = os.path.abspath(path)
        image = cv2.imread(absolute_path)

        if image is None:
            raise FileNotFoundError("Không thể mở file ảnh. Kiểm tra lại đường dẫn và tính toàn vẹn của file.")
        
        codes = decode(image)
        if len(codes) == 0:
            messagebox.showinfo("Kết quả", "Không tìm thấy nội dung QR/barcode")
        else:
            for code in codes:
                code_info = code.data.decode('utf-8')
                # print(code_info)
                if messagebox.askyesno("Kết quả", f"Nội dung: {code_info}. \n\nBạn có muốn sao chép nội dung này?"):
                    pyperclip.copy(code_info)
                fo.write(code_info + '\n')

    except FileNotFoundError as e:
        messagebox.showerror("File not found Error:", str(e))
    except Exception as e:
        messagebox.showerror("Error:", str(e))


def scan_from_camera():
    fo = open("readqr.txt", 'a', encoding='utf-8')

    # mở camera
    # tham số 0 đại diện cho camera chính
    # nếu có nhiều camera, thay thành số thích hợp
    cam = cv2.VideoCapture(0)
    found_code = False
    # lấy liên tục các khung hình từ camera, cho đến khi nhấn Esc
    while True:
        # ok chứa trạng thái thành công (True/ False)
        # frame chứa dữ liệu ảnh
        # cam.read() - đọc khung hình từ camera
        ok, frame = cam.read()

        # duyệt qua tất cả các khung hình có mã QR - barcode
        if not found_code:
            for code in decode(frame):
                # tạo một mảng numpy từ danh sách các điểm định nghĩa đa giác (polygon), với kiểu dữ liệu là np.int32
                pts = np.array([code.polygon], np.int32)
                # thay đổi hình dạng của mảng pts thành một mảng 3 chiều.
                # -1 trong hàm reshape cho phép numpy tính tự động kích thước của chiều đó dựa trên kích thước tổng thể của mảng.
                pts.reshape((-1, 1,2))
            
                # vẽ đường đa giác, dùng khung hình frame, tham số pts
                # True: là đường khép kín
                # (42, 157, 143): màu sắc của đường
                # 2: Độ dày của đường đa giác
                cv2.polylines(frame, [pts], True, (42, 157, 143), 2 )
                if code.type == 'QRCODE' or code.type == 'CODE128':
                    data = code.data.decode("utf-8")
                    if code.type == 'QRCODE':
                        messagebox.showinfo("Kết quả QR", f"Nội dung: {data}")
                    elif code.type == 'CODE128':
                        messagebox.showinfo("Kết quả Barcode", f"Nội dung: {data}")
                    fo.write(data + '\n')
                    found_code = True
        # Điều chỉnh lại để camera có thể nhận dạng liên tục            
        if found_code:
            found_code = False
     
            
        # hiển thị khung hình camera
        cv2.imshow("Barcode/QRcode frame", frame)

        # lưu thông tin phím bấm
        key_press = cv2.waitKey(1)
        
        # Bấm Esc để dừng camera
        if key_press == 27:
            break

    # Giải phóng bộ nhớ
    fo.close()
    cam.release()
    cv2.destroyAllWindows()
