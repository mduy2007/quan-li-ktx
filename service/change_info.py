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
        
       
        #lấy dữ liệu và tái sử dụng lại các hàm khác
        self.data = file_works(file_path="data/info_student.json")
        self.use_data = students_service
        self.seen_data = self.data.load_file()

        tieptuc = False
        #vòng lặp hiển thị sinh viên
        u = 0 #đặt giá trị để hiển thị
        self.all_student= []
        self.display_list_student = []
        if self.seen_data is None or len(self.seen_data) == 0:
            print("Dữ liệu đang trống! Vui lòng tạo")
        
        for info in self.seen_data.values():
                self.all_student.append(info) #lấy tất cả dữ liệu sinh viên đưa vào mảng all student
                
        page_student = self.all_student[u: u + 9] #hiện tại page_student đang chứa 9 sinh viên từ list all student

        if not page_student:
            print("Danh Sách Đã Hết!")
            return
                
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
        
            if self.display_list_student:
                    change = inquirer.fuzzy(
                        message="Vui Lòng Chọn Thông Tin Bạn Muốn Thay Đổi",
                        choices=[*self.display_list_student,
                        Choice(value='tieptuc',name='trang tiếp theo'),
                        Choice(value=None,name="Rời Khỏi")],
                        pointer='>',
                        default=None
                    ).execute()
                    if change is None:
                        print("Đã Thoát!")
                        break

                    if change == 'tieptuc':
                        tieptuc = True
                        u += 9
                        continue

                #Giới tính và cccd sẽ không thay đổi, nếu có sẽ xoá tạo lại
                    if change is not None:
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
                        xac_nhan5 = inquirer.confirm(
                            message="Bạn có muốn thay đổi phòng?",
                            mandatory=True,
                            default=True
                        ).execute()
                        while True:
                            if xac_nhan5 is False:
                                break
                            else: 
                                self.data2=file_works("data/dorm.json")
                                self.lay_du_lieu = self.data2.load_file()
                                for key,value in self.lay_du_lieu.items():
                                    for vlue in value:
                                        if vlue['count'] <= 10 and vlue['role'] == self.role[change]['role']:
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
                                    self.save_file(self.seen_data) #save vào file info_student.json - sử dụng hàm khác savedata để dễ lưu hơn
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
                                    self.data.save_file(saoluu) #save file vào dorm.json
                                    #Lưu dữ liệu đã thay đổi vào file chính
                                    self.save_file(self.seen_data) #save vào file info_student.json - sử dụng hàm khác savedata để dễ lưu hơn
                                    self.data.save_file(self.lay_du_lieu)
                
    #xoá thông tin sinh viên
    def delete_info(self):
        dulieu_sinhvien = []
        for i in self.all_student:
            dulieu_sinhvien.append(
                {
                'name': f"ID: {i['id']}    |   Tên: {i['name']}",
                'value': f"{i['id']}"
                }
            )
        if dulieu_sinhvien:
            del_info = inquirer.fuzzy(
                message="Vui Lòng Chọn Thông Tinh Sinh Viên Bạn Muốn Xoá: ",
                choices=[*dulieu_sinhvien, Choice(value=None,name= 'Thoát')]
            ).execute()
            if del_info is None:
                print("Thoát Thành Công!")
            else:
                dulieuxoa = del_info
                del self.seen_data[dulieuxoa]
                try:
                    print("Đã Xoá Thành Công!")
                except KeyError:
                    print("Xoá Thất Bại!")
            for key, value  in self.lay_du_lieu.items(): #lấy dự liệu trong file dorm.json
                for room in value:
                    room_c = f"{room['id_dorm']} - {room['id_room']}"
                    if room_c == del_info['dorm']:
                        room['count'] = int(room.get('count', 0)) - 1
                        break
                    break
            
            self.data.save_file(self.lay_du_lieu)
            self.save_file(self.seen_data)




        
        

        