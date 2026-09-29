from service.admin_service import info_dorm
from service.student_service import students_service
from service.change_info import  change
from service.student_service import file_works 
from service.staff_service import staff
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import bcrypt
import os
import json
from service.auth_service import save_pw


if __name__ == "__main__":
#     # print("test full")
#     print("""
# ╔══════════════════════════════════════════════╗
# ║   TOOL QUẢN LÍ SINH VIÊN KÍ TÚC XÁ           ║
# ╚══════════════════════════════════════════════╝
# """)
#     # save_pw()
#     print("Xác Thực Quyền ADMIN")
#     give_data = file_works(file_path="data/important.json")
#     load_pw = give_data.load_file()

#     name = input("Vui lòng nhập tên đăng nhập: ")
#     raw = inquirer.secret(
#         message="Nhập Mật Khẩu: ",
#         mandatory=True
#     ).execute()
    
#     password = raw.encode('utf-8')
#     pw = load_pw['pw'].encode('utf-8')
#     if name == load_pw['name_user'] and bcrypt.checkpw(password, pw):

#         while True:
#             print("--MENU--")
#             menu = inquirer.fuzzy(
#                 message="Vui lòng lựa chọn các chức năng sau: ",
#                 choices=[Choice(value=1, name = '1. thêm sinh viên'),
#                          Choice(value=2, name = '2. chỉnh sửa dữ liệu sinh viên'),
#                          Choice(value=3, name = '3. xoá thông tin sinh viên'),
#                          Choice(value=4, name = '4. Thêm thông tin kí túc xá'),
#                          Choice(value=5, name = '5. Tắt Menu')
#                          ],
#                 mandatory=True
#             ).execute()
#             if menu == 1:
#                 students_service(file_path='').add_info_student_in_dorm()
#                 continue
#             if menu == 2:
#                 change(file_path='').change_info_student()
#                 continue
#             if menu == 3:
#                 change(file_path='').delete_info()
#                 continue
#             if menu == 4:
#                 info_dorm(file_path='').add_dorm()
#                 continue
#             if menu == 5:
#                 print("Tắt Menu Thành Công")
#                 break
#     else:
#         print("Sai Thông Tin Đăng Nhập!")

    print("test lưu staff")
    staff(file_path='').add_staff()










    # info2 = students_service(file_path="")
    # info2.add_info_student_in_dorm()
    # info2.save_data()
    # print("Test quá trình lưu pass")
    # print(save_pw())
    # data = info_dorm(file_path="data/dorm.json")
    # nhapktx = data.add_dorm()
    # print("test thêm ktx")
    # print(nhapktx)