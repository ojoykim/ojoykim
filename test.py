# 버튼이 3개가 있고 첫번째 버튼을 누를 때는 체크박스 입력으로 받고 두번째 버튼을 누를 때는 라디오버튼으로 변경되고 세번째 버튼을 누를 때는 텍스트 입력창으로 변경되는 파이썬 코드

import tkinter as tk

def show_checkbox():
    clear_frame()
    checkbox = tk.Checkbutton(frame, text="Check me")
    checkbox.pack()

def show_radiobutton():
    clear_frame()
    radiobutton1 = tk.Radiobutton(frame, text="Option 1", value=1)
    radiobutton2 = tk.Radiobutton(frame, text="Option 2", value=2)
    radiobutton1.pack()
    radiobutton2.pack()

def show_entry():
    clear_frame()
    entry = tk.Entry(frame)
    entry.pack()

def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("Dynamic Widgets")

frame = tk.Frame(root)
frame.pack(pady=20)

button1 = tk.Button(root, text="Show Checkbox", command=show_checkbox)
button1.pack(side=tk.LEFT, padx=10)

button2 = tk.Button(root, text="Show Radiobutton", command=show_radiobutton)
button2.pack(side=tk.LEFT, padx=10)

button3 = tk.Button(root, text="Show Entry", command=show_entry)
button3.pack(side=tk.LEFT, padx=10)

root.mainloop()











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
