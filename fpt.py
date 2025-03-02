# import pandas as pd
# import json
# import serial
# import time
# import struct
# import tkinter as tk
# from tkinter import ttk

# class ProtocolConverter:
#     def __init__(self, excel_file, json_file):
#         self.excel_file = excel_file
#         self.json_file = json_file
#         self.df = self.read_excel()
    
#     def read_excel(self):
#         """
#         엑셀 파일을 읽고 JSON 파일로 변환하는 함수
#         """
#         try:
#             df = pd.read_excel(self.excel_file)
#             df.to_json(self.json_file, orient='records', indent=4)
#             return df
#         except FileNotFoundError:
#             print(f"Error: File '{self.excel_file}' not found.")
#             return pd.DataFrame()  # Return an empty DataFrame to prevent crashes        
    
#     def read_json(self):
#         """
#         JSON 파일을 읽어 DataFrame으로 변환하는 함수
#         """
#         with open(self.json_file, 'r') as file:
#             data = json.load(file)
#         return pd.DataFrame(data)
    
#     def pack_data(self, selected_command, selected_bitfields, selected_ranges):
#         df = self.read_json()
#         df = df[df['Command'] == selected_command]

#         bitfield = 0
#         total_bits = 0
#         byte_values = {}

#         for _, row in df.iterrows():
#             data_type = row['Data Type']
#             start_bit = int(row['Start Bit']) if pd.notna(row['Start Bit']) else None
#             data_length = int(row['Data Length']) if pd.notna(row['Data Length']) else 1
#             data_name = row['Data']

#             if data_type == 'Bit Field' and start_bit is not None:
#                 value = int(selected_bitfields.get(data_name, 0))  # 체크된 항목만 1
#                 bitfield |= (value & ((1 << data_length) - 1)) << start_bit
#                 total_bits = max(total_bits, start_bit + data_length)

#             elif data_type == 'Range' and start_bit is not None:
#                 value = int(selected_ranges.get(data_name, 0))
#                 byte_index = start_bit // 8
#                 byte_values[byte_index] = value

#         total_bytes = (total_bits + 7) // 8
#         packed_bitfield = struct.pack(f">{'BHIQ'[total_bytes - 1]}", bitfield)
        
#         final_data = bytearray(packed_bitfield)
        
#         for index, value in byte_values.items():
#             struct.pack_into('>B', final_data, index, value)

#         return bytes(final_data)

# class UARTCommunicator:
#     def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
#         self.port = port
#         self.baudrate = baudrate
    
#     def send(self, binary_data):
#         """
#         바이너리 데이터를 UART를 통해 전송하는 함수
#         """
#         try:
#             ser = serial.Serial(self.port, self.baudrate, timeout=1)
#             time.sleep(2)  # UART 안정화 대기
            
#             ser.write(binary_data)
#             ser.close()
#             print("UART 전송 완료!")
#         except Exception as e:
#             print(f"UART 전송 실패: {e}")
    
#     def receive(self):
#         """
#         UART에서 데이터 수신 (모의 수신)
#         """
#         try:
#             ser = serial.Serial(self.port, self.baudrate, timeout=1)
#             received_data = ser.read(8)  # 8바이트 읽기 (예제)
#             ser.close()
#             return received_data.hex()
#         except Exception as e:
#             print(f"UART 수신 실패: {e}")
#             return None

# class CommandUI:
#     def __init__(self, root, protocol_converter, uart_communicator):
#         self.protocol_converter = protocol_converter
#         self.uart_communicator = uart_communicator
#         self.root = root
#         self.root.title("Command Selection")
#         self.root.geometry("700x500")
        
#         self.df = self.protocol_converter.read_json()
#         self.commands = list(self.df['Command'].unique())
#         self.selected_command = tk.StringVar()
#         self.selected_command.trace("w", self.update_data_fields)
        
#         self.selected_bitfields = {}
#         self.selected_ranges = {}
        
#         self.create_widgets()
    
#     def create_widgets(self):
#         main_frame = ttk.Frame(self.root)
#         main_frame.pack(fill=tk.BOTH, expand=True)
        
#         # Command Frame (왼쪽)
#         command_frame = ttk.Frame(main_frame)
#         command_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
#         ttk.Label(command_frame, text="Select Command:").pack()
        
#         self.command_dropdown = ttk.Combobox(command_frame, textvariable=self.selected_command, values=self.commands, state="readonly", height=5)
#         self.command_dropdown.pack()
        
#         self.send_button = ttk.Button(command_frame, text="Send Command", command=self.send_selected_command)
#         self.send_button.pack()
        
#         # Data Frame (오른쪽)
#         self.data_frame = ttk.Frame(main_frame)
#         self.data_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
# def update_data_fields(self, *args):
#     """선택한 명령어에 따라 비트필드 및 범위 슬라이더를 동적으로 UI에 표시"""
#     # 기존 위젯 제거 (이전 선택 항목 지우기)
#     for widget in self.data_frame.winfo_children():
#         widget.destroy()

#     command = self.selected_command.get()
#     if not command:
#         return

#     df = self.df[self.df['Command'] == command]
#     self.selected_bitfields.clear()
#     self.selected_ranges.clear()

#     bitfield_frame = ttk.LabelFrame(self.data_frame, text="Bit Fields")
#     bitfield_frame.pack(fill='x', padx=5, pady=5)

#     range_frame = ttk.LabelFrame(self.data_frame, text="Range Values")
#     range_frame.pack(fill='x', padx=5, pady=5)

#     for _, row in df.iterrows():
#         data_name = row['Data']
#         data_type = row['Data Type']
#         start_bit = row['Start Bit']

#         # ✅ 여러 개의 비트 필드 체크박스 추가
#         if data_type == 'Bit Field' and pd.notna(start_bit):
#             var = tk.IntVar(value=0)  # 체크 기본값 0
#             chk = ttk.Checkbutton(bitfield_frame, text=data_name, variable=var)
#             chk.pack(anchor='w', padx=5, pady=2)
#             self.selected_bitfields[data_name] = var  # ✅ 여러 개의 Bit Field 저장 가능하게 수정!

#         # ✅ 여러 개의 범위 슬라이더 추가 (정수 값 유지)
#         elif data_type == 'Range':
#             min_value = int(row['Min']) if 'Min' in row and pd.notna(row['Min']) else 0
#             max_value = int(row['Max']) if 'Max' in row and pd.notna(row['Max']) else 255

#             var = tk.IntVar(value=min_value)  # ✅ 정수 값 유지
#             frame = ttk.Frame(range_frame)
#             frame.pack(fill='x', padx=5, pady=2)

#             # 최소값 표시
#             min_label = ttk.Label(frame, text=f"{min_value}")
#             min_label.pack(side="left", padx=5)

#             # ✅ 슬라이더 이벤트 핸들러 추가 (정수 값 변환)
#             def update_var(value, v=var, s=None):
#                 int_value = int(float(value))
#                 v.set(int_value)  # tk.IntVar 값 업데이트
#                 if s:  # Spinbox 값도 업데이트
#                     s.delete(0, "end")
#                     s.insert(0, str(int_value))

#             # 슬라이더 (정수 값 설정, tk.IntVar 사용)
#             slider = ttk.Scale(frame, from_=min_value, to=max_value, variable=var, command=lambda v: update_var(v))
#             slider.pack(side="left", expand=True, fill='x', padx=5)

#             # Spinbox 추가 (정수 조정 가능)
#             spinbox = ttk.Spinbox(frame, from_=min_value, to=max_value, textvariable=var, increment=1, width=5)
#             spinbox.pack(side="right", padx=5)

#             # 슬라이더 값을 Spinbox와 동기화
#             slider.config(command=lambda v, s=spinbox: update_var(v, var, s))

#             # 최대값 표시
#             max_label = ttk.Label(frame, text=f"{max_value}")
#             max_label.pack(side="right", padx=5)

#             self.selected_ranges[data_name] = var  # ✅ 여러 개의 Range 저장 가능하게 수정!




    
#     def send_selected_command(self):
#         command = self.selected_command.get()
#         if not command:
#             print("No command selected.")
#             return
        
#         binary_data = self.protocol_converter.pack_data(command, {}, {})
#         self.uart_communicator.send(binary_data)
#         received_data = self.uart_communicator.receive()
        
#         print(f"Sent: {binary_data.hex()}")
#         if received_data:
#             print(f"Received: {received_data}")

# if __name__ == "__main__":
#     excel_file = "commands.xlsx"
#     json_file = "protocol_spec.json"
    
#     converter = ProtocolConverter(excel_file, json_file)
#     uart = UARTCommunicator()
    
#     root = tk.Tk()
#     app = CommandUI(root, converter, uart)
#     root.mainloop()



# import readchar

# def show_menu():
#     menu_items = {
#         "1": "옵션 1",
#         "2": "옵션 2",
#         "3": "옵션 3",
#         "e": "프로그램 종료"
#     }

#     while True:
#         print("\n=== 메뉴 선택 ===")
#         for key, value in menu_items.items():
#             print(f"{key}. {value}")

#         print("\n키를 눌러 선택하세요...", end="", flush=True)
#         choice = readchar.readkey()  # 즉시 키 입력 받기

#         if choice in menu_items:
#             print(f"\n{menu_items[choice]}을 선택했습니다.")
#             if choice == "e":
#                 break
#         else:
#             print("\n잘못된 입력입니다.")

# if __name__ == "__main__":
#     show_menu()
