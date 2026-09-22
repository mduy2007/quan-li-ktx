# from service.student_service import students_service
from service.admin_service import info_student

if __name__ == "__main__":
    # info = students_service(file_path="data/info_student.json")
    # data = info.add_info_student()
    # print("Test quá trình lưu pass")
    # print(save_pw())
    # print("test thêm sinh viên")
    # print(data)

    data = info_student(file_path="data/dorm.json")
    nhapktx = data.add_dorm()
    print("test thêm ktx")
    print(nhapktx)