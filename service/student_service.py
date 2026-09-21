#Xây Dựng Dịch Vụ Dành Cho Student

"""Các Dịch Vụ Bao Gồm Như Sau:
- Tạo mới, thay đổi, xoá thông tinh sinh viên: Họ Tên, MSSV, CCCD, Mã Lớp, Phòng Ở, Toà Ở"""
#tạo đường dẫn file và import
import os
import json
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
class file_works:
    #tiến hành tạo nếu chưa có file
    def __init__(self, file_path):
        #hàm tạo
        self.file_path = file_path
        dir_name = os.path.dirname(self.file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

    def load_file(self):
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_file(self,data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data,file,ensure_ascii=False,indent=4)
            print(f"đã lưu dữ liệu vào {self.file_path} thành công!")

#tutorial use class file_works
"""
lấy dữ liệu từ file
data_student = file_works(data/data_student.json)

đọc dữ liệu từ file
list_student = data_student.load_file()

save dữ liệu vào file
data_student.save_file(data_input)
"""

class students_service(file_works):
    #hàm khởi tạo lại dữ liệu từ class cha file_works
    def __init__(self, file_path):
            super().__init__(file_path)
            #thêm dữ liệu vào dict
            self.dulieu = self.load_file()
    def add_info_student(self):

        #bảng dict
        """info = {
            'name': 'name',
            'id': 'mssv',
            'cccd': 'cccd',
            'id_class': 'ma_lop',
            'id_room': 'phong_o',
            'id_dorm': 'toa_o'
        } """
        
        #vòng lặp thêm thông tin sinh viên
        while True:
            self.id_student = input("Vui Lòng Nhập Mssv: ").strip()
            if self.id_student in (st['id'] for st in self.dulieu):
                print("ID nãy đã tồn tại!") 
                continue
            else:
                break

        self.name_student = input("Vui Lòng Nhập Tên: ")

        while True:
            self.cccd= input(" Vui Lòng Nhập Thông Tin CCCD: ").strip().upper()
            if len(self.cccd) < 12 or len(self.cccd) > 12:
                print("Thông tin căn cước công dân của bạn không đúng!")
                continue
            else:
                print(f"Đã Ghi Nhận, Dãy Số CCCD Bạn Vừa Nhập Là: {self.cccd}")
                self.new_data = inquirer.confirm(
                    message=("Bạn có muốn nhập lại dữ liệu không? "),
                    default=False
                ).execute()
                if self.new_data == True:
                    continue
                else:
                    break
                
        self.id_class = input("Vui Lòng Nhập Mã Lớp: ")

        self.id_room = input("Vui Lòng Nhập Phòng Ở: ")

        self.id_dorm = input(" Vui Lòng Chọn Toà: ")

        self.dulieu.append({'name': self.name_student, 'id': self.id_student, 'CCCD': self.cccd, 'id_class': self.id_class, 'id_room': self.id_room, 'id_dorm': self.id_dorm})

        self.save_file(self.dulieu)
        return self.dulieu