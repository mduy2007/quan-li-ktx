import bcrypt
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from service.admin_service import info_dorm
from service.change_info import change
from service.student_service import file_works, students_service
from service.staff_service import staff


ADMIN_CREDENTIALS_PATH = "data/important.json"

def setup_admin_credentials():
    """Chỉ chạy 1 lần, sau đó xoá hàm này đi, để tránh lộ thông tin đăng nhập quản trị."""
    print("Thiết lập thông tin đăng nhập quản trị.")
    name_user = input("Vui lòng nhập tên đăng nhập: ").strip()
    password = inquirer.secret(
        message="Nhập Mật Khẩu: ",
        mandatory=True,
    ).execute()

    # Hash the password before storing it
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    credentials = {
        "name_user": name_user,
        "pw": password_hash,
    }
    file_works(ADMIN_CREDENTIALS_PATH).save_file(credentials)
    return


def authenticate_admin() -> bool:
    """Ask for the admin credentials and verify the stored password hash."""
    credentials = file_works(ADMIN_CREDENTIALS_PATH).load_file()
    if not isinstance(credentials, dict):
        print("Không thể đọc thông tin đăng nhập quản trị.")
        return False

    username = credentials.get("name_user")
    password_hash = credentials.get("pw")
    if not isinstance(username, str) or not isinstance(password_hash, str):
        print("Thông tin đăng nhập quản trị không hợp lệ.")
        return False

    print("Xác Thực Quyền ADMIN")
    entered_username = input("Vui lòng nhập tên đăng nhập: ").strip()
    entered_password = inquirer.secret(
        message="Nhập Mật Khẩu: ",
        mandatory=True,
    ).execute()

    if entered_username == username and bcrypt.checkpw(
        entered_password.encode("utf-8"),
        password_hash.encode("utf-8"),
    ):
        return True

    print("Sai Thông Tin Đăng Nhập!")
    return False


def run_admin_menu() -> None:
    """Show the available management actions and dispatch the selected one."""
    actions = {
        "add_student": (
            "Thêm sinh viên",
            lambda: students_service("data/info_student.json").add_info_student_in_dorm(),
        ),
        "edit_student": (
            "Chỉnh sửa thông tin sinh viên",
            lambda: change("data/info_student.json").change_info_student(),
        ),
        "delete_student": (
            "Xóa sinh viên",
            lambda: change("data/info_student.json").delete_info(),
        ),
        "add_dorm": (
            "Thêm thông tin ký túc xá",
            lambda: info_dorm("data/dorm.json").add_dorm(),
        ),
        "add_staff": (
            "Thêm nhân viên",
            lambda: staff("data/staff.json").add_staff(),
        ),
        "calculate_salary": (
            "Tính lương nhân viên",
            lambda: staff("data/staff.json").salary(),
        ),
    }

    choices = [
        Choice(value=action, name=label)
        for action, (label, _) in actions.items()
    ]
    choices.append(Choice(value="exit", name="Thoát"))

    while True:
        selected_action = inquirer.select(
            message="Vui lòng chọn chức năng:",
            choices=choices,
            mandatory=True,
        ).execute()

        if selected_action == "exit":
            print("Đã thoát chương trình.")
            return

        _, run_action = actions[selected_action]
        run_action()


def main() -> None:
    print(
        """
╔══════════════════════════════════════════════╗
║   TOOL QUẢN LÝ SINH VIÊN KÝ TÚC XÁ          ║
╚══════════════════════════════════════════════╝
"""
    )
    if authenticate_admin():
        run_admin_menu()


if __name__ == "__main__":
    main()
