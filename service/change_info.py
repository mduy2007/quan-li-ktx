"""
Thay đổi thông tin sinh viên, nhân viên
"""
from service.student_service import file_works
from service.student_service import students_service
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

#thay đổi thông tin nhân viên
class change(file_works):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.dulieu = self.load_file

    def change_info_student(self):
        
        self.display_list_student = []
        #lấy dữ liệu và tái sử dụng lại các hàm khác
        self.data = file_works(file_path="data/info_student.json")
        self.use_data = students_service
        self.taisudunghamsave = self.use_data.save_data()
        self.seen_data = self.data.load_file()


        #vòng lặp hiển thị sinh viên
        u = 0 #đặt giá trị để hiển thị
        for key, info in self.seen_data:
            if self.seen_data is None:
                print("Dữ liệu đang trống! Vui lòng tạo")
                break
            else:
                for i in range(len(info)):
                    for j in range(u, u + 9):
                        try: 
                            self.thongtin = info[j]
                            self.display_list_student.append (
                                {
                                    'name': f"ID: {self.thongtin['id']}  |   Tên: {self.thongtin['name']}",
                                    'value': self.thongtin['id']
                                }
                            )
                        except IndexError:
                            print("Đã hết danh sách!")
                            break
                        u += 9
                if self.display_list_student:
                    change = inquirer.fuzzy(
                        message="Vui Lòng Chọn Thông Tin Bạn Muốn Thay Đổi",
                        choices=[*self.display_list_student,
                        Choice(value=None,name="Thoát")],
                        pointer='>',
                        default=None
                    ).execute()
                print("Bạn đã chọn sinh viên: " + change)
                #Giới tính và cccd sẽ không thay đổi, nếu có sẽ xoá tạo lại
                if change is not None:
                    while True:
                        xac_nhan1 = inquirer.confirm(
                            message="Bạn có muốn thay đổi tên?",
                            default=True
                        ).execute()
                        if xac_nhan1 is False:
                            break
                        name = input("Nhập Tên Thay Đổi: ")
                        if name == "":
                            print("Trường tên không được để trống!")
                            continue
                        else:
                            print("Nhập tên thành công, tên bạn vừa nhập là " + name)
                            self.seen_data[change]['name'] = name #thay thế vào phần tử đã chọn
                            break
                    while True:
                        xac_nhan3 = inquirer.confirm(
                            message="Bạn có muốn thay đổi Mã Lớp?",
                            default=True
                        ).execute()
                        if xac_nhan3 is False:
                            break
                        id_class = input("Nhập Mã Lớp: ")
                        if id_class == "":
                            print("Mã Lớp không được để trống")
                            continue
                        else:
                            print("Nhập thành công, mã lớp bạn vừa nhập là: "+id_class)
                            self.seen_data[change]['class'] = id_class
                            break
                    
                    
                    #thay đổi phòng ở
                    while True:
                        xac_nhan5 = inquirer.confirm(
                            message="Bạn có muốn thay đổi phòng?",
                            mandatory=True,
                            default=True
                        ).execute()
                        if xac_nhan5 is False:
                            break
                        else: 
                            self.data2=file_works("data/dorm.json")
                            self.lay_du_lieu = self.data2.load_file()
                            for key,value in self.lay_du_lieu.items():
                                for vlue in value:
                                    if vlue['count'] <= 10 and vlue['role'] == self.role:
                                        self.data_select.append(
                                            {
                                                "name": f"Phòng {vlue['id_dorm']}.{vlue['id_room']} hiện có {vlue['count']}",
                                                "value": f"{vlue['id_dorm']} - {vlue['id_room']}"
                                            }
                                        )
                    
                            if self.data_select:
                                self.id_dorm = inquirer.fuzzy(
                                    message="Vui lòng chọn phòng bạn cần ở:",
                                    choices=self.data_select,
                                    multiselect=False,
                                    mandatory=True
                                ).execute()
                                self.seen_data[change]['id_dorm'] = self.id_dorm

                                #Lưu dữ liệu đã thay đổi vào file chính
                                self.taisudunghamsave(self.seen_data) #Lưu thành công vào file
                                #cập nhật số lượng
                               #Trừ cũ
                                saoluu = self.seen_data[change]['dorm'] 
                                for key, value  in self.lay_du_lieu.items():
                                    for room in value:
                                        room_c = f"{room['id_dorm']} - {room['id_room']}"
                                        if room_c == self.id_dorm:
                                            room['count'] = int(room.get('count', 0)) - 1
                                            break
                                        break

                                check = False
                                for key,value in self.lay_du_lieu.items():

                                    for room in value:
                                            room_c = f"{room['id_dorm']} - {room['id_room']}"
                                            if room_c == self.id_dorm:
                                                room['count'] = int(room.get('count', 0)) + 1
                                                check = True
                                                break
                                    if check:
                                        break

                                #sử dụng hàm save_file từ file W
                                self.data.save_file(saoluu,self.seen_data)
                    #change hiện đang là thứ mà user đã chọn, đồng thời cũng là key trong dict, bây giờ chỉ việc lôi nó ra, thay đổi theo vòng lặp trong list của dict, sau đó save_file là xong!

                if self.display_list_student:
                    check_list = inquirer.confirm(
                        message="Bạn có muốn tiếp tục đến trang kế?",
                        default=True
                    ).execute()
                    if check_list:
                        continue
                    else:
                        print("Thoát Thành Công!")
                        break
                break
        
        

        