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
        self.du_lieu_tong = []
    
    #hàm khởi tạo lại id nếu trường hợp id bị mất, bị lỗi, có thể chỉ khởi chạy lần đầu
    #tự động tạo id và tăng dần nó
     def first_id_staff(self):
            if not self.load_data:
                return 1
            return max(int(id_staff) for id_staff in self.load_data.keys()) + 1

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
          self.cache_staff = self.load_data if self.load_data else {}
          self.data_staff = file_works(file_path="data/staff.json")
          self.cache_staff[self.first_id_staff()] = {
               'MaNV': self.add_id(id_NV),
               'name_staff': name,
               'role': vitri,
          }
          #lưu file
          self.data_staff.save_file(self.cache_staff)

     def salary(self):    #tính lương
        
          time_tuple = time.gmtime()
          self.data_salary = file_works(f"data/salary/{time.strftime('%Y_%m', time_tuple)}.json")
          self.data_staff = file_works(file_path="data/staff.json")
          self.load_salary = self.data_salary.load_file()
          self.load_data = self.data_staff.load_file()
          
          dict_salary = {
                    'Quản lí': 19871270,
                    'Trực Ban':18872000,
                    'Nhân Viên Ban Kỷ Luật': 9821092,
                    'Buôn Bán Canteent': 6982000,
                    'Bảo Vệ': 11982021,
                    'Lao Công': 5981721
          } 
          locale.setlocale(locale.LC_ALL, 'vi-VN')

          #Tính toán lương tháng và lưu vào salary/ xxxx.json
          staff = []
          count = 1
          for key, i in self.load_data.items():
                    staff.append(
                         {
                         'name': f"Tên: {i['name_staff']}   |   Công Việc: {i['role']}",
                         'value': count
                         }
                    )
                    count  += 1

          ket_toan = inquirer.fuzzy(
               message="Chọn Vị Trí Cần Kết Toán Lương:",
               choices=[*staff,
                         Choice(value=-1,name='Tất Cả'),
                         Choice(value=-2,name='Thoát')
                         ],
               mandatory=True,
               default=0
          ).execute()

          he_so_ot = {
               1: 150,
               2: 200,
               3: 310
          }

          count_data = 1
          for k in dict_salary.keys():
               found = False
               if str(k) == self.load_data[str(ket_toan)]['role']:
                    #Nhập ngày thực làm
                    while True:
                         try:
                              days = int(input('Nhập Số Ngày Thực Làm: '))
                         except ValueError:
                              print("Số Ngày Không Hợp Lệ!")
                              continue
                         if days < 0 or days > 31:
                              print("Số ngày đi làm không hợp lệ")
                              continue
                         else:
                              break
                         
                    for key,v in dict_salary.items():
                         if key == self.load_data[str(ket_toan)]['role']:
                              one_h = (v / 24) / 8  #lương 1h
                              salary_role = (one_h * 8) * days
                              tong_luong_sau_chuyen_doi = locale.currency(salary_role, symbol=False, grouping=True)
                              print(f"Lương Cơ Bản Của Nhân Viên {self.load_data[str(ket_toan)]['name_staff']}   |   Vị Trí {self.load_data[str(ket_toan)]['role']}: {tong_luong_sau_chuyen_doi}")
                    while True:
                         ot = inquirer.fuzzy(
                              message='Vui Lòng Chọn Loại OT',
                              choices=[Choice(value=1, name='Ngày Thường'),
                                   Choice(value=2, name='Ngày Nghỉ'),
                                   Choice(value=3, name='Lễ Tết'),
                                   Choice(value=4, name='Không Có')],
                                   mandatory=True
                         ).execute()

                         if ot == 4:
                              break
                         
                         time_ot = float(input("Nhập số giờ OT: "))
                         
                         one_h_OT = (one_h * he_so_ot[ot]) / 100
                         salary_role += one_h_OT * time_ot
                         tong_luong_sau_chuyen_doi = locale.currency(salary_role, symbol=False, grouping=True)
                         
                                                       
                         cf = inquirer.confirm(
                              message='Tiếp tục chọn?',
                              default=False,
                              mandatory=True
                         ).execute()
                         if cf is False:
                              found = True
                              break
               
                    self.du_lieu_tong.append(
                         {
                              'Name': self.load_data[str(count_data)]['name_staff'],
                              'Role': self.load_data[str(count_data)]['role'],
                              'Salary': tong_luong_sau_chuyen_doi
                         }
                    )      
                    if count > count_data:
                         count_data += 1
                    #luu vào file
                    self.data_salary.save_file(self.du_lieu_tong)
               elif ket_toan == -1:
                    for keys, values in dict_salary.items():
                         for khoa, gia_tri in self.load_data.items():
                              if gia_tri['role'] == keys:
                                   ten = (input(f'Vui lòng nhập số ngày làm cho nhân viên {gia_tri['name']}   |    Vị trí {gia_tri['role']}: '))

                                   if not isinstance(ten, (float, int)):
                                        raise ValueError('định dạng đầu vào không hợp lệ')
                                   
                                   one_h = (values / 24) / 8
                                   luong = (one_h * 8) * ten
                                   tong_luong_sau_chuyen_doi = locale.currency(luong, symbol=False, grouping=True)

                                   self.du_lieu_tong.append(
                                        {
                                             'Name': gia_tri['name_staff'],
                                             'Role': gia_tri['role'],
                                             'Salary': tong_luong_sau_chuyen_doi
                                        }
                                   )         
                                   self.data_salary.save_file(self.du_lieu_tong)
          
               elif ket_toan == -2:
                    break

               elif found:
                    break

         