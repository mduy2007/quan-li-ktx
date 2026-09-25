from service.admin_service import info_dorm
from service.student_service import students_service
from service.student_service import file_works 
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import bcrypt
import os
import json
from service.auth_service import save_pw


if __name__ == "__main__":
    # print("test full")
    
    # save_pw()
    print("Xác Thực Quyền ADMIN")
    give_data = file_works(file_path="data/important.json")
    load_pw = give_data.load_file()

    name = input("Vui lòng nhập tên đăng nhập: ")
    raw = inquirer.secret(
        message="Nhập Mật Khẩu: ",
        mandatory=True
    ).execute()
    
    password = raw.encode('utf-8')
    pw = load_pw['pw'].encode('utf-8')
    if name == load_pw['name_user'] and bcrypt.checkpw(password, pw):

        while True:
            print("--MENU--")
            menu = inquirer.fuzzy(
                message="Vui lòng lựa chọn các chức năng sau: ",
                choices=[
                    "1. Thêm Sinh Viên",
                    "2. Chỉnh sửa Thông Tin Sinh Viên",
                    "3. Thêm Thông Tin Kí Túc Xá",
                ],
                mandatory=True
            ).execute()
    else:
        print("Sai Thông Tin Đăng Nhập!")

           










    # info2 = students_service(file_path="")
    # info2.add_info_student_in_dorm()
    # info2.save_data()
    # print("Test quá trình lưu pass")
    # print(save_pw())
    # data = info_dorm(file_path="data/dorm.json")
    # nhapktx = data.add_dorm()
    # print("test thêm ktx")
    # print(nhapktx)