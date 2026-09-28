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
        self.dulieu = self.load_file()

    def change_info_student(self):
        #lấy dữ liệu và tái sử dụng lại các hàm khác
        self.data = file_works(file_path="data/info_student.json")
        self.use_data = students_service
        self.seen_data = self.data.load_file() or {}

       
        #vòng lặp hiển thị sinh viên
        u = 0 #đặt giá trị để hiển thị
        self.all_student= []
        
        if self.seen_data is None or len(self.seen_data) == 0:
            print("Dữ liệu đang trống! Vui lòng tạo")
        
        for info in self.seen_data.values():
                self.all_student.append(info) #lấy tất cả dữ liệu sinh viên đưa vào mảng all student
        while True:
            tieptuc = False
            self.display_list_student = []
            page_student = self.all_student[u: u + 9] #hiện tại page_student đang chứa 9 sinh viên từ list all student
            
            if not page_student:
                print("Danh Sách Đã Hết!")
                break
            for j in page_student:
                try:    
                    thongtin = j
                    self.display_list_student.append (
                        {
                            'name': f"ID: {thongtin['id']}  |   Tên: {thongtin['name']}",
                            'value': thongtin['id']
                        }
                    )
                except KeyError: # Lỗi nếu trong dict sinh viên thiếu trường 'id' hoặc 'name'
                    print("File Hỏng hoặc Dữ liệu sinh viên thiếu cấu trúc!")
                    break
                except Exception as e:
                    print(f"Có lỗi xảy ra: {e}")
                    break
                thoat = False
            if self.display_list_student:
                    change = inquirer.fuzzy(
                        message="Vui Lòng Chọn Thông Tin Bạn Muốn Thay Đổi",
                        choices=[*self.display_list_student,
                        Choice(value='tieptuc',name='trang tiếp theo'),
                        Choice(value=None,name="Rời Khỏi")],
                        pointer='>',
                        default=None
                    ).execute()

                    if change == 'tieptuc':
                        tieptuc = True
                        print("Chuyển Trang Thành Công!")
                        
                    
                    if change is not None and change != 'tieptuc':
                    #Giới tính và cccd sẽ không thay đổi, nếu có sẽ xoá tạo lại
                        print("Bạn đã chọn sinh viên: " + change)
                        xac_nhan1 = inquirer.confirm(
                            message="Bạn có muốn thay đổi tên?",
                            default=True
                        ).execute()
                        while True:
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
                        xac_nhan3 = inquirer.confirm(
                            message="Bạn có muốn thay đổi Mã Lớp?",
                            default=True
                        ).execute()
                        while True:
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
                        self.data_select = []
                        self.data2=file_works("data/dorm.json")
                        self.lay_du_lieu = self.data2.load_file()
                        xac_nhan5 = inquirer.confirm(
                            message="Bạn có muốn thay đổi phòng?",
                            mandatory=True,
                            default=True
                        ).execute()
                        while True:
                            dachonphong = False
                            if xac_nhan5 is False:
                                break
                            else: 
                                for key,value in self.lay_du_lieu.items():
                                    for vlue in value:
                                        if vlue['count'] <= 10 and vlue['role'] == self.seen_data[change]['role']:
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

                                    dachonphong = True

                                #Trừ cũ
                                    frag = False
                                    for key, value  in self.lay_du_lieu.items():
                                        for room in value:
                                            room_c = f"{room['id_dorm']} - {room['id_room']}"
                                            if room_c == self.seen_data[change]['dorm']:
                                                room['count'] = int(room.get('count', 0)) - 1
                                                frag = True
                                                break
                                        if frag:
                                            break
                                    self.seen_data[change]['dorm'] = self.id_dorm
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
                                if dachonphong:
                                    break
                            
                                #sử dụng hàm save_file từ file W
                                #Lưu dữ liệu đã thay đổi vào file chính
                        self.data.save_file(self.seen_data) #save vào file info_student.json - sử dụng hàm khác savedata để dễ lưu hơn
                        self.data2.save_file(self.lay_du_lieu)
                    if change is None:
                        print("Đã Thoát!")
                        thoat = True
                        break
            if thoat:
                break
            if tieptuc:
                u += 9
                continue #chạy lại vòng lặp 1 lần nữa để load dữ liệu mới
        
                
    #xoá thông tin sinh viên
    def delete_info(self):
        self.data3 = file_works(file_path='data/info_student.json')
        self.data4 = file_works(file_path="data/dorm.json")
        self.lay_du_lieu_phong = self.data4.load_file()
        self.lay_du_lieu_xoa = self.data3.load_file()
        self.dulieu_sinhvien = []
        for key,i in self.lay_du_lieu_xoa.items():
            self.dulieu_sinhvien.append(
                {
                'name': f"ID: {i['id']}    |   Tên: {i['name']}",
                'value': f"{i['id']}"
                }
            )
        if self.dulieu_sinhvien:
            del_info = inquirer.fuzzy(
                message="Vui Lòng Tìm Thông Tinh Sinh Viên Bạn Muốn Xoá: ",
                choices=[*self.dulieu_sinhvien, Choice(value=None,name= 'Thoát')],
                default=None
            ).execute()
            if del_info is None:
                print("Thoát Thành Công!")
                
            else:
                try:
                    print("Đã Xoá Thành Công!")
                except KeyError:
                    print("Xoá Thất Bại!")
            found_old = False
            for key, value  in self.lay_du_lieu_phong.items(): #lấy dự liệu trong file dorm.json
                for room in value:
                    room_c = f"{room['id_dorm']} - {room['id_room']}"
                    if room_c == self.lay_du_lieu_xoa[del_info]['dorm']:
                        room['count'] = int(room.get('count', 0)) - 1
                        found_old = True
                        dulieuxoa = del_info
                        del self.lay_du_lieu_xoa[dulieuxoa] #xoá dữ liệu khi trừ xong
                        break
                if found_old:
                    break
            
            self.data3.save_file(self.lay_du_lieu_xoa)
            self.data4.save_file(self.lay_du_lieu_phong)