"""
Thêm: Tên, Họ, Mã Nhân Viên, Lương, vị trí làm việc
mã nhân viên: bắt đầu từ KTX00 (3 số tiếp theo theo thứ tự từ 01)
vị trí làm việc: Quản Lí, Trực Ban, ban Kỷ Luật, buôn bán canteen, bảo vệ, lao công
lương:                           | Ngày làm việc|    Giờ Làm Việc
- Quản Lí: 19.871.270 vnđ        |   24 days    |        8h
- Trực Ban: 18.872.000 vnđ       |   30 days    |        6h
- ban kỷ luật: 9.821.092         |   30 days    |        6h
- buôn bán canteen: 6.982.000    |   30 days    |        8h
- Bảo Vệ: 11.982.021             |   30 days    |        12h
- Lao Công: 5.981.721            |   30 days    |        6h
công thức tính giờ lương:
Lương 1h = (Lương Tháng)
            -----------  / số giờ làm việc
              Số Ngày
Quy tắc OT:
Ngày Thường: up 150% lương
Ngày nghỉ:   up 200% lương
Lễ, Tết, Nghỉ có lương: 310% lương + lương ngày nghỉ vẫn tính
Vị trí không cho phép OT: ngày thường/ngày nghỉ: bảo vệ 
"""
from service.student_service import file_works
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import locale
import os
import time

class staff(file_works):
    def __init__(self, file_path):
        super().__init__(file_path)
        folder = 'data/salary'
        os.makedirs(folder, exist_ok=True)
        self.load_data = self.load_file()
        self.load_salary = self.load_file()
    
    #hàm khởi tạo lại id nếu trường hợp id bị mất, bị lỗi, có thể chỉ khởi chạy lần đầu
    #tự động tạo id và tăng dần nó
    def first_id_staff(self):
            if not self.load_data:
                return 1
            return max(id_staff['id'] for id_staff in self.load_data) + 1

    #Mã Nhân Viên
    def add_id(self, num_id):
         #cú pháp formax theo thứ tự tăng dần có giới hạn và tự sinh số 0 ở đầu
         return f"KTX{num_id:05d}"
         
    def add_staff(self):
        #mở file
        self.data_staff = file_works(file_path="data/staff.json")
        self.load_data = self.data_staff.load_file()
        #tạo dữ liệu 
        self.cache_staff = {} #cache lưu dữ liệu nhân viên tạm thời vào để nạp vào file

        #thêm thông tin
        while True:
             name = input("Nhập Tên Nhân Viên: ").strip().title()
             if name == "":
                  print("Tên Không Thể Để Trống!")
                  continue
             elif name.replace(" ","").isalpha() is False: #check xem tên có kí tự đặc biện không, replace thay các kí tự khoảng trắng thành kí tự dính sát
                  print("Tên Không Chứa Kí Tự Đặc Biệt!")
                  continue
             else:
                  print("Nhập Thành Công! Tên Vừa Nhập Là: " + name)
                  break
            
        #Chọn Vị Trí

        vitri = inquirer.select(
             message="Vui Lòng Chọn Vị Trí Làm Việc Của Nhân Viên Này:",
             choices=[
                'Quản lí',
                'Trực Ban',
                'Thành Viên Ban Kỷ luật',
                'Buôn Bán Canteent',
                'Bảo Vệ',
                'Lao Công',
             ],
             mandatory=True
        ).execute()

        id_NV = self.first_id_staff()
        self.cache_staff[self.first_id_staff()] = {
             'MaNV': self.add_id(id_NV),
             'name_staff': name,
             'role': vitri,
        }
        print(self.cache_staff)

        #lưu file
        self.data_staff.save_file(self.cache_staff)

    # def salary(self):
        
    #     time_tuple = time.gmtime()
    #     self.data_salary = file_works(f"data/salary/{time.strftime('%Y_%m', time_tuple)}.json")
    #     self.load_salary = self.data_salary
    #     self.load_data = self.data_staff
        
    #     dict_salary = [
    #           {
    #             'quanli': 19871270,
    #             'trucban':18872000,
    #             'bankyluat': 9821092,
    #             'buonbancanteent': 6982000,
    #             'baove': 11982021,
    #             'laocong': 5981721
    #           }
    #     ]
    #     locale.setlocale(locale.LC_ALL, 'vi-VN')

    #     #Tính toán lương tháng và lưu vào salary/ xxxx.json
    #     for i in self.load_data.items():
             



