# from service.admin_service import info_dorm
from service.student_service import students_service

if __name__ == "__main__":
    print("test thêm sinh viên")

    info2 = students_service(file_path="")
    info2.add_info_student_in_dorm()
    info2.save_data()
    
    


    
    # print("Test quá trình lưu pass")
    # print(save_pw())
    # data = info_dorm(file_path="data/dorm.json")
    # nhapktx = data.add_dorm()
    # print("test thêm ktx")
    # print(nhapktx)