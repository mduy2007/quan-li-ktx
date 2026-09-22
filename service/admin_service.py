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
class info_dorm(file_works):
    def __init__(self, file_path):
        #tái sử dụng
        self.dulieu = {} #tạo dict rỗng để đưa vào file(đưa vào init để chỉ khởi tạo 1 lần, tránh ghi đè dữ liệu chung)
        self.dorm = file_works(file_path="data/dorm.json")
        super().__init__(file_path)
        #load dữ liệu
        self.data =  self.dorm.load_file() or {} # có thể dùng cách này nếu như hệ thống nhận diện self.data là list không phải dict

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


        #role giới tính
        self.gioi_tinh = inquirer.select(
            message="Vui Lòng Chọn Giới Tính Cho Toà Này: ",
            choices=["nam", "nữ"],
            mandatory=True,
            mandatory_message="Trường này bắt buộc chọn"
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
        #xây dựng vòng lặp add người vào ktx


        #xây dựng vòng lặp thêm dữ liệu vào file json
        self.count = 0
        u = 0
        for i in range(self.so_tang):
            self.ket_noi = ["Tầng",i+1] #ghép tầng và số lại với nhau
            self.nhap_lai = " ".join(map(str, self.ket_noi))
            for j in range(u, u + 12):
                dorm_data = {       #đưa dữ liệu nhập vào dict
                        "id_dorm": self.dorm_phase2,
                        "id_floor": self.nhap_lai,
                        "role": self.gioi_tinh,
                        "id_room": self.so_phong[j],
                        "count": self.count
                    }
                self.dulieu.setdefault(self.dorm_phase2, []).append(dorm_data) #set mặc định là toà G, bởi vì G là mặc định trong suốt quá trình chạy, nếu vậy thì dữ liệu sẽ hiểu sai và chỉ lưu dữ liệu cuối cùng, đây là 1 phương pháp
            u += 12
        self.data.update(self.dulieu)
        self.save_file(self.data)
        return self.data     




    #count = 1
    #ây ui fix xong rồi