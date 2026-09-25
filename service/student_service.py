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
            return {}

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
            super().__init__(file_path="data/info_student.json")
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
            if self.id_student in self.dulieu:
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

        role = inquirer.select(
            message="Giới tính của bạn là?",
            choices=["nam","nữ"]
        ).execute()

        return role
    
        #đưa lựa chọn từ file vào dict
    def add_info_student_in_dorm(self):
        self.role = self.add_info_student() #không cần vẫn được, nhưng nguyên tắc là code đã chạy là không động
        self.data_select = []
        self.doc_du_lieu = file_works("data/dorm.json")
        self.lay_du_lieu = self.doc_du_lieu.load_file()
        #dòng debug tạm thời
        if self.lay_du_lieu is None:
            self.lay_du_lieu = {}
        if not isinstance(self.lay_du_lieu, dict):
            self.lay_du_lieu = {}

        for key,value in self.lay_du_lieu.items():
            for vlue in value:
                if vlue['count'] <= 10 and vlue['role'] == self.role:
                    self.data_select.append(
                        {
                            "name": f"Phòng {vlue['id_dorm']}.{vlue['id_room']} hiện có {vlue['count']}",
                            "value": f"{vlue['id_dorm']} - {vlue['id_room']}"
                        }
                    )

        if self.data_select:
            self.id_dorm = inquirer.fuzzy(
                message="Vui lòng chọn phòng bạn cần ở:",
                choices=self.data_select,
                multiselect=False
            ).execute()
        else:
            self.id_dorm = None

        #xây dựng hàm so sánh 2 đối tượng để + số lượng cho count ở dorm.json
        if self.id_dorm is not None: #đặt giá trị id_domrm khác none để nếu user kh chọn điều kiện sẽ không chạy
            found = False #đặt cờ
            for key,rooms in self.lay_du_lieu.items(): #lấy mảng trong dict ra
                if not isinstance(rooms, list):
                    print("Lỗi! File Json Không phải dict, vui lòng tải lại") #nếu file rooms không phải dict thì in ra để tắt chương trình
                    continue
                else:
                    for room in rooms: #đặt 1 vòng lặp nữa để so sánh
                        room_count = f"{room['id_dorm']} - {room['id_room']}"

                        if room_count == self.id_dorm:
                            room['count'] = int(room.get('count', 0)) + 1
                            found = True
                            break
                    if found:
                        break
        self.save_data()
        self.doc_du_lieu.save_file(self.lay_du_lieu)
    def save_data(self):
        self.dulieu[self.id_student] = {
            'id': self.id_student,
            'role': self.role,
            'name': self.name_student,
            'id_human': self.cccd,
            'class': self.id_class,
            "dorm": self.id_dorm
        }
        self.save_file(self.dulieu)
        return self.dulieu