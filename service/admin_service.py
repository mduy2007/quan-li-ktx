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
        #Thêm Toà Ktx
        self.ki_tuc_xa = inquirer.number (
            message="Vui Lòng Nhập Toà: ".strip(),
            mandatory=True,
            float_allowed=False,
            mandatory_message="Trường này buộc nhập",
            validate=lambda val: val is not None or "Số Toà Không Hợp Lệ!"
        ).execute()
        self.dorm_phase1 = ["G", self.ki_tuc_xa]
        self.dorm_phase2 = "".join(map(str,self.dorm_phase1))

        #thêm số tầng
        self.floor = inquirer.number (
            message="Vui Lòng Nhập Số Tầng: ".strip(),
            mandatory=True,
            float_allowed=False,
            mandatory_message="Trường này là bắt buộc!",
            validate=lambda val: val is not None or "Số Tầng Không Hợp Lệ!"
        ).execute()

        #tự động sinh thêm số phòng theo tầng đã nhập
        self.so_phong = []
        self.so_tang = int(self.floor)
        for i in range(self.so_tang):
            for j in range(12):
                if j < 9:
                    self.ghep = [i+1,j+1]
                    self.nhap = "0".join(map(str, self.ghep))
                    self.so_phong.append(self.nhap)
                else:
                    self.ghep = [i+1,j+1]
                    self.nhap = "".join(map(str, self.ghep))
                    self.so_phong.append(self.nhap)
        #xây dựng vòng lặp thêm dữ liệu vào file json
        u = 0
        for i in range(self.so_tang):
            self.ket_noi = ["Tầng",i+1]
            self.nhap_lai = " ".join(map(str, self.ket_noi))
            for j in range(u, u + 12):
                self.data.append(
                    {
                        "id_dorm": self.dorm_phase2,
                        "id_floor": self.nhap_lai,
                        "id_room": self.so_phong[j]
                    
                    }
                )
            u += 12
        self.save_file(self.data)
        return self.data     