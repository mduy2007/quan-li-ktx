from auth.account import Account #nhập class vào
import bcrypt
import os
import json
FILE_PATH = "data/important.json"
acc = Account() # đặt biến acc thành class Account


#hàm lưu pass vào file important
def save_pw():
    pw, name_user = acc.setup() #gọi method của object đó cho người dùng nhập liệu

    hashed = bcrypt.hashpw(pw, bcrypt.gensalt(rounds=12)).decode("utf-8")   #băm pass ra để không dò được
                                                                            #decode để chuyển sang str, muốn chạy trở lại thì phải encode

    admin = {"pw": hashed,"name_user": name_user}

    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(admin, f, ensure_ascii=False, indent=4)
            print("Đã Lưu Dữ Liệu Thành Công!")
    return "đã chạy được!"