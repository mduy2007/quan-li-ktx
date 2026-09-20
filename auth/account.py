class Account:          #sử dụng class để tránh lỗi UnboundLocalError
    def __init__(self):   
        self.pw = None
        self.name_user = None

    def setup(self):
        if self.pw is None:
            self.pw = input("Vui Lòng Khởi Tạo Mật Khẩu: ").encode("utf-8")
            self.name_user = "Admin"
        return self.pw, self.name_user

   