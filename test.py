
import tkinter as tk
from tkinter import ttk
import serial
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class UARTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UART Communication")

        self.serial_port = None
        self.data = []
        self.volume = 1.0

        self.create_widgets()
        self.setup_plot()

    def create_widgets(self):
        self.port_label = ttk.Label(self.root, text="COM Port:")
        self.port_label.grid(row=0, column=0, padx=5, pady=5)
        self.port_entry = ttk.Entry(self.root)
        self.port_entry.grid(row=0, column=1, padx=5, pady=5)

        self.baudrate_label = ttk.Label(self.root, text="Baudrate:")
        self.baudrate_label.grid(row=1, column=0, padx=5, pady=5)
        self.baudrate_entry = ttk.Entry(self.root)
        self.baudrate_entry.grid(row=1, column=1, padx=5, pady=5)

        self.data_label = ttk.Label(self.root, text="Data bits:")
        self.data_label.grid(row=2, column=0, padx=5, pady=5)
        self.data_entry = ttk.Entry(self.root)
        self.data_entry.grid(row=2, column=1, padx=5, pady=5)

        self.stop_label = ttk.Label(self.root, text="Stop bits:")
        self.stop_label.grid(row=3, column=0, padx=5, pady=5)
        self.stop_entry = ttk.Entry(self.root)
        self.stop_entry.grid(row=3, column=1, padx=5, pady=5)

        self.parity_label = ttk.Label(self.root, text="Parity:")
        self.parity_label.grid(row=4, column=0, padx=5, pady=5)
        self.parity_entry = ttk.Entry(self.root)
        self.parity_entry.grid(row=4, column=1, padx=5, pady=5)

        self.open_button = ttk.Button(self.root, text="Connect", command=self.open_port)
        self.open_button.grid(row=5, column=0, padx=5, pady=5)

        self.close_button = ttk.Button(self.root, text="Disconnect", command=self.close_port)
        self.close_button.grid(row=5, column=1, padx=5, pady=5)

        self.send_button = ttk.Button(self.root, text="Send", command=self.send_data)
        self.send_button.grid(row=6, column=0, padx=5, pady=5)

        self.data_entry = ttk.Entry(self.root)
        self.data_entry.grid(row=6, column=1, padx=5, pady=5)

        self.volume_label = ttk.Label(self.root, text="Volume:")
        self.volume_label.grid(row=7, column=0, padx=5, pady=5)
        self.volume_slider = ttk.Scale(self.root, from_=0, to=1, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(1.0)
        self.volume_slider.grid(row=7, column=1, padx=5, pady=5)

        self.terminal = tk.Text(self.root, height=10, width=50)
        self.terminal.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        self.save_button = ttk.Button(self.root, text="Save Data", command=self.save_data)
        self.save_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

    def setup_plot(self):
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'r-')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(-10, 10)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=10, column=0, columnspan=2)

    def open_port(self):
        port = self.port_entry.get()
        baudrate = int(self.baudrate_entry.get())
        data_bits = int(self.data_entry.get())
        stop_bits = int(self.stop_entry.get())
        parity = self.parity_entry.get()

        self.serial_port = serial.Serial(port, baudrate, bytesize=data_bits, stopbits=stop_bits, parity=parity)
        self.terminal.insert(tk.END, f"Opened {port} at {baudrate} baud\n")

        self.read_thread = threading.Thread(target=self.read_data)
        self.read_thread.start()

    def close_port(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.terminal.insert(tk.END, "Closed port\n")

    def send_data(self):
        if self.serial_port and self.serial_port.is_open:
            data = self.data_entry.get()
            self.serial_port.write(data.encode())
            self.terminal.insert(tk.END, f"Sent: {data}\n")

    def read_data(self):
        while self.serial_port and self.serial_port.is_open:
            data = self.serial_port.readline().decode().strip()
            self.terminal.insert(tk.END, f"Received: {data}\n")
            self.data.append(float(data) * self.volume)
            self.update_plot()

    def update_plot(self):
        self.line.set_xdata(np.arange(len(self.data)))
        self.line.set_ydata(self.data)
        self.ax.set_xlim(0, len(self.data))
        self.canvas.draw()

    def set_volume(self, val):
        self.volume = float(val)

    def save_data(self):
        np.savetxt("data.csv", self.data, delimiter=",")
        self.terminal.insert(tk.END, "Data saved to data.csv\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = UARTApp(root)
    root.mainloop()














# import tkinter as tk
# from tkinter import ttk
# import serial
# import threading

# class UARTApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("UART Communication")

#         self.serial_port = None

#         self.create_widgets()

#     def create_widgets(self):
#         self.port_label = ttk.Label(self.root, text="COM Port:")
#         self.port_label.grid(row=0, column=0, padx=5, pady=5)
#         self.port_entry = ttk.Entry(self.root)
#         self.port_entry.grid(row=0, column=1, padx=5, pady=5)

#         self.baudrate_label = ttk.Label(self.root, text="Baudrate:")
#         self.baudrate_label.grid(row=1, column=0, padx=5, pady=5)
#         self.baudrate_entry = ttk.Entry(self.root)
#         self.baudrate_entry.grid(row=1, column=1, padx=5, pady=5)

#         self.data_label = ttk.Label(self.root, text="Data bits:")
#         self.data_label.grid(row=2, column=0, padx=5, pady=5)
#         self.data_entry = ttk.Entry(self.root)
#         self.data_entry.grid(row=2, column=1, padx=5, pady=5)

#         self.stop_label = ttk.Label(self.root, text="Stop bits:")
#         self.stop_label.grid(row=3, column=0, padx=5, pady=5)
#         self.stop_entry = ttk.Entry(self.root)
#         self.stop_entry.grid(row=3, column=1, padx=5, pady=5)

#         self.parity_label = ttk.Label(self.root, text="Parity:")
#         self.parity_label.grid(row=4, column=0, padx=5, pady=5)
#         self.parity_entry = ttk.Entry(self.root)
#         self.parity_entry.grid(row=4, column=1, padx=5, pady=5)

#         self.open_button = ttk.Button(self.root, text="OPEN", command=self.open_port)
#         self.open_button.grid(row=5, column=0, padx=5, pady=5)

#         self.close_button = ttk.Button(self.root, text="CLOSE", command=self.close_port)
#         self.close_button.grid(row=5, column=1, padx=5, pady=5)

#         self.send_button = ttk.Button(self.root, text="Send", command=self.send_data)
#         self.send_button.grid(row=6, column=0, padx=5, pady=5)

#         self.data_entry = ttk.Entry(self.root)
#         self.data_entry.grid(row=6, column=1, padx=5, pady=5)

#         self.terminal = tk.Text(self.root, height=10, width=50)
#         self.terminal.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

#     def open_port(self):
#         port = self.port_entry.get()
#         baudrate = int(self.baudrate_entry.get())
#         data_bits = int(self.data_entry.get())
#         stop_bits = int(self.stop_entry.get())
#         parity = self.parity_entry.get()

#         self.serial_port = serial.Serial(port, baudrate, bytesize=data_bits, stopbits=stop_bits, parity=parity)
#         self.terminal.insert(tk.END, f"Opened {port} at {baudrate} baud\n")

#         self.read_thread = threading.Thread(target=self.read_data)
#         self.read_thread.start()

#     def close_port(self):
#         if self.serial_port and self.serial_port.is_open:
#             self.serial_port.close()
#             self.terminal.insert(tk.END, "Closed port\n")

#     def send_data(self):
#         if self.serial_port and self.serial_port.is_open:
#             data = self.data_entry.get()
#             self.serial_port.write(data.encode())
#             self.terminal.insert(tk.END, f"Sent: {data}\n")

#     def read_data(self):
#         while self.serial_port and self.serial_port.is_open:
#             data = self.serial_port.readline().decode()
#             self.terminal.insert(tk.END, f"Received: {data}\n")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = UARTApp(root)
#     root.mainloop()








# 200바이트 정도의 값을 입력받아 UI에서 십진수 십육진수를 선택하고 exclusive Or 또는 add sum 또는 16bit CCITT crc값을 tkinter로구하는 파이썬 코드

# import tkinter as tk
# from tkinter import ttk
# import binascii

# def calculate():
#     data = entry.get().encode()
#     operation = operation_var.get()
#     base = base_var.get()
    
#     if base == "Decimal":
#         data = int(data)
#     elif base == "Hexadecimal":
#         data = int(data, 16)
    
#     if operation == "Exclusive OR":
#         result = data ^ 0xFFFF  # Example XOR operation
#     elif operation == "Add Sum":
#         result = sum(data)
#     elif operation == "16bit CCITT CRC":
#         result = crc16_ccitt(data)
    
#     result_var.set(f"Result: {result}")

# def crc16_ccitt(data: bytes):
#     crc = 0xFFFF
#     for byte in data:
#         crc ^= byte << 8
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ 0x1021
#             else:
#                 crc <<= 1
#             crc &= 0xFFFF
#     return crc

# root = tk.Tk()
# root.title("Data Operation")

# frame = ttk.Frame(root, padding="10")
# frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# entry = ttk.Entry(frame, width=50)
# entry.grid(row=0, column=1, padx=5, pady=5)

# operation_var = tk.StringVar()
# operation_menu = ttk.OptionMenu(frame, operation_var, "Exclusive OR", "Exclusive OR", "Add Sum", "16bit CCITT CRC")
# operation_menu.grid(row=1, column=1, padx=5, pady=5)

# base_var = tk.StringVar()
# base_menu = ttk.OptionMenu(frame, base_var, "Decimal", "Decimal", "Hexadecimal")
# base_menu.grid(row=2, column=1, padx=5, pady=5)

# calculate_button = ttk.Button(frame, text="Calculate", command=calculate)
# calculate_button.grid(row=3, column=1, padx=5, pady=5)

# result_var = tk.StringVar()
# result_label = ttk.Label(frame, textvariable=result_var)
# result_label.grid(row=4, column=1, padx=5, pady=5)

# root.mainloop()

















# 버튼이 3개가 있고 첫번째 버튼을 누를 때는 체크박스 입력으로 받고 두번째 버튼을 누를 때는 라디오버튼으로 변경되고 세번째 버튼을 누를 때는 텍스트 입력창으로 변경되는 파이썬 코드

# import tkinter as tk

# def show_checkbox():
#     clear_frame()
#     checkbox = tk.Checkbutton(frame, text="Check me")
#     checkbox.pack()

# def show_radiobutton():
#     clear_frame()
#     radiobutton1 = tk.Radiobutton(frame, text="Option 1", value=1)
#     radiobutton2 = tk.Radiobutton(frame, text="Option 2", value=2)
#     radiobutton1.pack()
#     radiobutton2.pack()

# def show_entry():
#     clear_frame()
#     entry = tk.Entry(frame)
#     entry.pack()

# def clear_frame():
#     for widget in frame.winfo_children():
#         widget.destroy()

# root = tk.Tk()
# root.title("Dynamic Widgets")

# frame = tk.Frame(root)
# frame.pack(pady=20)

# button1 = tk.Button(root, text="Show Checkbox", command=show_checkbox)
# button1.pack(side=tk.LEFT, padx=10)

# button2 = tk.Button(root, text="Show Radiobutton", command=show_radiobutton)
# button2.pack(side=tk.LEFT, padx=10)

# button3 = tk.Button(root, text="Show Entry", command=show_entry)
# button3.pack(side=tk.LEFT, padx=10)

# root.mainloop()











# import tkinter as tk

# def toggle_widgets():
#     if checkbutton.winfo_viewable():
#         checkbutton.grid_remove()
#         radiobutton.grid_remove()
#         entry.grid_remove()
#     else:
#         checkbutton.grid()
#         radiobutton.grid()
#         entry.grid()

# root = tk.Tk()
# root.title("Toggle Widgets")

# # 체크박스
# chk_var = tk.IntVar()
# checkbutton = tk.Checkbutton(root, text="체크박스", variable=chk_var)
# checkbutton.grid(row=0, column=0, padx=10, pady=10)

# # 라디오 버튼
# radio_var = tk.IntVar()
# radiobutton = tk.Radiobutton(root, text="라디오 버튼", variable=radio_var, value=1)
# radiobutton.grid(row=1, column=0, padx=10, pady=10)

# # 텍스트 입력창
# entry = tk.Entry(root)
# entry.grid(row=2, column=0, padx=10, pady=10)

# # 토글 버튼
# toggle_button = tk.Button(root, text="토글", command=toggle_widgets)
# toggle_button.grid(row=3, column=0, padx=10, pady=10)

# root.mainloop()



















# import tkinter as tk
# import json

# # JSON 데이터 예시
# data = '''
# {
#     "checkboxes": ["Option 1", "Option 2", "Option 3"],
#     "radiobuttons": ["Choice A", "Choice B", "Choice C"]
# }
# '''

# # JSON 데이터를 파싱
# parsed_data = json.loads(data)

# # Tkinter 윈도우 생성
# root = tk.Tk()
# root.title("Checkboxes and Radiobuttons")

# # 체크박스 생성
# checkbox_vars = []
# for option in parsed_data["checkboxes"]:
#     var = tk.IntVar()
#     checkbox = tk.Checkbutton(root, text=option, variable=var)
#     checkbox.pack(anchor='w')
#     checkbox_vars.append(var)

# # 라디오 버튼 생성
# radio_var = tk.IntVar()
# for idx, choice in enumerate(parsed_data["radiobuttons"]):
#     radiobutton = tk.Radiobutton(root, text=choice, variable=radio_var, value=idx)
#     radiobutton.pack(anchor='w')

# # Tkinter 메인 루프 실행
# root.mainloop()











# import tkinter as tk
# from tkinter import ttk
# import serial

# class UARTApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("UART 설정 GUI")
        
#         self.port_label = ttk.Label(root, text="포트:")
#         self.port_label.grid(column=0, row=0, padx=10, pady=10)
#         self.port_entry = ttk.Entry(root)
#         self.port_entry.grid(column=1, row=0, padx=10, pady=10)
        
#         self.baud_label = ttk.Label(root, text="보드레이트:")
#         self.baud_label.grid(column=0, row=1, padx=10, pady=10)
#         self.baud_entry = ttk.Entry(root)
#         self.baud_entry.grid(column=1, row=1, padx=10, pady=10)
        
#         self.connect_button = ttk.Button(root, text="연결", command=self.connect)
#         self.connect_button.grid(column=0, row=2, columnspan=2, padx=10, pady=10)
        
#         self.serial_connection = None

#     def connect(self):
#         port = self.port_entry.get()
#         baudrate = self.baud_entry.get()
#         try:
#             self.serial_connection = serial.Serial(port, baudrate)
#             print(f"연결 성공: {port} @ {baudrate}")
#         except Exception as e:
#             print(f"연결 실패: {e}")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = UARTApp(root)
#     root.mainloop()





# import serial
# import serial.tools.list_ports
# import tkinter as tk
# from tkinter import ttk

# def list_ports():
#     ports = serial.tools.list_ports.comports()
#     return [port.device for port in ports]

# def connect():
#     port = port_var.get()
#     baudrate = int(baudrate_var.get())
#     ser = serial.Serial(port, baudrate)
#     ser.write(b'Hello UART\n')
#     response = ser.readline()
#     print(f"Received: {response.decode('utf-8')}")
#     ser.close()

# # GUI 설정
# root = tk.Tk()
# root.title("UART 통신 설정")

# # 포트 선택 콤보박스
# port_var = tk.StringVar()
# ports = list_ports()
# port_label = tk.Label(root, text="COM 포트:")
# port_label.pack()
# port_combo = ttk.Combobox(root, textvariable=port_var, values=ports)
# port_combo.pack()

# # 보드레이트 선택 콤보박스
# baudrate_var = tk.StringVar()
# baudrate_label = tk.Label(root, text="보드레이트:")
# baudrate_label.pack()
# baudrate_combo = ttk.Combobox(root, textvariable=baudrate_var, values=["9600", "19200", "38400", "57600", "115200"])
# baudrate_combo.pack()

# # 연결 버튼
# connect_button = tk.Button(root, text="연결", command=connect)
# connect_button.pack()

# root.mainloop()
