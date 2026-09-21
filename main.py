from service.student_service import students_service

if __name__ == "__main__":
    info = students_service(file_path="data/info_student.json")
    data = info.add_info_student()
    # print("Test quá trình lưu pass")
    # print(save_pw())
    print("test thêm sinh viên")
    print(data)