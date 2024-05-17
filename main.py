# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from PIL import Image, ImageTk
import detect
import create

class App:
    def __init__(self, root):
        self.bc = False
        self.qr = False
        
        # setting title
        root.title("QR Code/Barcode APP")
        # setting window size
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.configure(bg="#f0f0f0")

        ft_label = tkFont.Font(family='Poppins', size=16, weight='bold')
        ft_entry = tkFont.Font(family='Poppins', size=12)
        ft_button = tkFont.Font(family='Poppins', size=12, weight='bold')

        self.label1 = tk.Label(root, text="QR/ BarCode Generator", font=ft_label, fg="#333333", bg="#f0f0f0")
        self.label1.pack(pady=20)

        entry_frame = tk.Frame(root, bg="#f0f0f0")
        entry_frame.pack(pady=10, padx=20, fill=tk.X)

        self.txtBox = tk.Entry(entry_frame, font=ft_entry, fg="#333333", relief=tk.SOLID, borderwidth=1)
        self.txtBox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.btn_clear = tk.Button(entry_frame, text="Clear", font=ft_button, bg="#FF0000", fg="#ffffff", relief=tk.RAISED, borderwidth=2, command=self.clear_text)
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(root, width=500, height=250, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.qr_image = None

        self.btn_generate_qr = tk.Button(root, text="Generate QR Code", font=ft_button, bg="#007BFF", fg="#ffffff", relief=tk.RAISED, borderwidth=2, command=self.generate_qr_code)
        self.btn_generate_qr.pack(side=tk.LEFT, padx=20, pady=20)
        self.btn_generate_qr.bind("<Enter>", lambda e: self.on_hover(e, self.btn_generate_qr, "#0056b3"))
        self.btn_generate_qr.bind("<Leave>", lambda e: self.on_hover_leave(e, self.btn_generate_qr, "#007BFF"))

        self.btn_generate_barcode = tk.Button(root, text="Generate Barcode", font=ft_button, bg="#007BFF", fg="#ffffff", relief=tk.RAISED, borderwidth=2, command=self.generate_barcode)
        self.btn_generate_barcode.pack(side=tk.LEFT, padx=20, pady=20)
        self.btn_generate_barcode.bind("<Enter>", lambda e: self.on_hover(e, self.btn_generate_barcode, "#0056b3"))
        self.btn_generate_barcode.bind("<Leave>", lambda e: self.on_hover_leave(e, self.btn_generate_barcode, "#007BFF"))

        self.btn_scan = tk.Button(root, text="Scan QR/Barcode", font=ft_button, bg="#28a745", fg="#ffffff", relief=tk.RAISED, borderwidth=2, command=self.scan_code)
        self.btn_scan.pack(side=tk.RIGHT, padx=20, pady=20)
        self.btn_scan.bind("<Enter>", lambda e: self.on_hover(e, self.btn_scan, "#218838"))
        self.btn_scan.bind("<Leave>", lambda e: self.on_hover_leave(e, self.btn_scan, "#28a745"))

    def on_hover(self, event, widget, color):
        widget.config(bg=color)

    def on_hover_leave(self, event, widget, color):
        widget.config(bg=color)

    def clear_text(self):
        self.txtBox.delete(0, tk.END)
        self.canvas.delete("all")

    def generate_qr_code(self):
        entry_text = self.txtBox.get()
        if entry_text:
            image_path = create.show_qr_code(entry_text)
            self.display_image(image_path)
        else:
            messagebox.showwarning("Warning", "Please enter data before proceeding.")
            self.txtBox.focus_set()

    def generate_barcode(self):
        entry_text = self.txtBox.get()
        if entry_text:
            image_path = create.show_barcode(entry_text)
            self.display_image(image_path)
        else:
            messagebox.showwarning("Warning", "Please enter data before proceeding.")
            self.txtBox.focus_set()

    def scan_code(self):
        detect.scan_option()

    def display_image(self, image_path):
        if image_path is not None:

            self.canvas.delete("all")
            image = Image.open(image_path)
            image = image.resize((250, 250), Image.LANCZOS)
            self.qr_image = ImageTk.PhotoImage(image)

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            center_x = canvas_width / 2
            center_y = canvas_height / 2

            self.canvas.create_image(center_x, center_y, image=self.qr_image, anchor=tk.CENTER) 

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()



# OLD VERSION

"""
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import detect
import create

class App:
    def __init__(self, root):
        self.bc = False
        self.qr = False
        #setting title
        root.title("QRcode/Barcode APP")
        #setting window size
        width=600
        height=400
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.btn1=tk.Button(root)
        self.btn1["bg"] = "#01aaed"
        ft = tkFont.Font(family='Times',size=13)
        self.btn1["font"] = ft
        self.btn1["fg"] = "#000000"
        self.btn1["justify"] = "center"
        self.btn1["text"] = "Tạo QR code"
        self.btn1.place(x=50,y=140,width=120,height=45)
        self.btn1["command"] = self.btn1_command

        label1=tk.Label(root)
        label1["anchor"] = "center"
        ft = tkFont.Font(family='Times',size=22)
        label1["font"] = ft
        label1["fg"] = "#333333"
        label1["justify"] = "center"
        label1["text"] = "Generate and Scan QRcode/barcode"
        label1.place(x=70,y=20,width=470,height=75)

        self.btn2=tk.Button(root)
        self.btn2["bg"] = "#00ced1"
        ft = tkFont.Font(family='Times',size=13)
        self.btn2["font"] = ft
        self.btn2["fg"] = "#000000"
        self.btn2["justify"] = "center"
        self.btn2["text"] = "Tạo Barcode"
        self.btn2.place(x=240,y=140,width=120,height=45)
        self.btn2["command"] = self.btn2_command

        btn3=tk.Button(root)
        btn3["bg"] = "#fad400"
        ft = tkFont.Font(family='Times',size=13)
        btn3["font"] = ft
        btn3["fg"] = "#000000"
        btn3["justify"] = "center"
        btn3["text"] = "Quét QR/Barcode"
        btn3.place(x=410,y=140,width=150,height=45)
        btn3["command"] = self.btn3_command

        self.txtBox=tk.Entry(root)
        self.txtBox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=13)
        self.txtBox["font"] = ft
        self.txtBox["fg"] = "#333333"
        self.txtBox["justify"] = "left"
        self.txtBox["text"] = ""
        self.txtBox.config(state='disabled')
        self.txtBox.place(x=170,y=230,width=254,height=30)

        btn4=tk.Button(root)
        btn4["bg"] = "#e4ffe4"
        ft = tkFont.Font(family='Times',size=13)
        btn4["font"] = ft
        btn4["fg"] = "#000000"
        btn4["justify"] = "center"
        btn4["text"] = "Xác nhận"
        btn4.place(x=250,y=340,width=100,height=35)
        btn4["command"] = self.btn4_command

    def enable_button(self):
        self.btn1.config(state='normal')
        self.btn2.config(state='normal')

    def enable_textbox(self):
        self.txtBox.config(state='normal')

    def disable_textbox(self):
        self.txtBox.config(state='disabled')

    def btn1_command(self):
        self.enable_textbox()
        self.txtBox.focus_set()
        self.qr = True
        self.btn2.config(state='disabled')

    def btn2_command(self):
        self.enable_textbox()
        self.txtBox.focus_set()
        self.bc = True
        self.btn1.config(state='disabled')

    def btn3_command(self):
        detect.scan_option()
        self.enable_button()
        self.disable_textbox()

    def btn4_command(self):
        entry_text = self.txtBox.get()
        if entry_text:
            if self.qr == True:
                create.show_qr_code(entry_text)
                self.txtBox.delete(0, tk.END)
                self.disable_textbox()
                self.qr = False
            elif self.bc == True:
                create.show_barcode(entry_text)
                self.txtBox.delete(0, tk.END)
                self.disable_textbox()
                self.bc = False
            self.enable_button()
        else:
            messagebox.showwarning("Warning", "Please enter data before proceeding.")
            self.txtBox.focus_set()
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
"""