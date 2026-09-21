"""
Xây dựng các tính năng của admin, bao gồm:
quản lí Tạo, sửa, xoá thông tin sinh viên, nhân viên, Toà, Phòng
xây dựng hàm tạo file lưu trữ thông tin toà ở
quản lí điện, nước toà ở, thành tiền
"""

from service.student_service import file_works
from service.student_service import students_service
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

#Tái sử dụng hàm mở file
class info_student(file_works):
    def __init__(self, file_path):
        #tái sử dụng
        self.dorm = file_works(file_path="data/dorm.json")
        super().__init__(file_path)
        #load dữ liệu
        self.data =  self.load_file()

    #hàm thêm kí túc xá
    def add_dorm(self):
        self.ki_tuc_xa = inquirer.text (
            message="Vui Lòng Nhập Số Toà: ",
            mandatory=True,
            mandatory_message="Trường này buộc nhập"
        ).execute()
        #tự động sinh thêm số phòng theo tầng đã nhập
        self.so_phong = []
        self.so_toa = int(self.ki_tuc_xa)
        for i in range(self.so_toa):
            for j in range(12):
                if j < 9:
                    self.ghep = [i+1,j+1]
                    self.nhap = "0".join(map(str, self.ghep))
                    self.so_phong.append(self.nhap)
                else:
                    self.ghep = [i+1,j+1]
                    self.nhap = "".join(map(str, self.ghep))
                    self.so_phong.append(self.nhap)
        #tạo vòng lặp thêm vào dict
        """
        Định dạng vòng lặp:
        [
            G1
            [
                101
                ...
                112
            ]
            ...
        ]
        """

