# وارد کردن ابزارهای گرافیکی PyQt6 برای طراحی فرم
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QVBoxLayout, QHBoxLayout, QDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from data_base import DataBase  # ایمپورت کلاس پایگاه داده

# کلاس مربوط به فرم ورود مدیر
class ManagerLogin(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()  # راه‌اندازی رابط گرافیکی

    def setup_ui(self):
        # استایل پس‌زمینه فرم
        self.setStyleSheet("""
            background-color: #f8f9fa;
        """)

        # چیدمان افقی کلی فرم
        outer_layout = QHBoxLayout(self)
        fixed_left_widget = QWidget()
        fixed_left_widget.setFixedSize(450, 500)  # اندازه ثابت پنل سفید
        fixed_left_widget.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
            padding: 30px;
        """)

        fixed_left_layout = QVBoxLayout(fixed_left_widget)
        fixed_left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fixed_left_layout.setSpacing(25)

        # عنوان "ورود مدیر"
        self.label = QLabel("ورود مدیر")
        self.label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.label.setStyleSheet("""
            color: #2c3e50;
            padding-bottom: 10px;
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fixed_left_layout.addWidget(self.label)

        # استایل ورودی‌ها (نام کاربری، رمز عبور)
        input_style = """
            QLineEdit {
                font-size: 14px;
                border: 2px solid #dfe6e9;
                border-radius: 8px;
                padding: 12px 15px;
                min-width: 250px;
                background-color: #f8f9fa;
                color: #2d3436;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: white;
            }
            QLineEdit:hover {
                border: 2px solid #b2bec3;
            }
        """

        # چیدمان فرم
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        # فیلد نام کاربری
        self.username = QLineEdit()
        self.username.setFont(QFont('Arial', 14))
        self.username.setPlaceholderText("نام کاربری")
        self.username.setStyleSheet(input_style)
        form_layout.addWidget(self.username)

        # فیلد رمز عبور
        self.password = QLineEdit()
        self.password.setFont(QFont('Arial', 14))
        self.password.setPlaceholderText("رمز عبور")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet(input_style)
        self.password.returnPressed.connect(self.check_login)
        form_layout.addWidget(self.password)

        # استایل دکمه‌ها
        button_style = """
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                min-width: 120px;
                color: white;
                margin: 5px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:pressed {
                opacity: 0.8;
            }
        """

        # چیدمان دکمه‌ها (ورود، برگشت)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        # دکمه برگشت
        self.back_button = QPushButton("برگشت")
        self.back_button.setFont(QFont('Arial', 14))
        self.back_button.setStyleSheet(button_style + """
            QPushButton {
                background-color: #e74c3c;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.back_button.clicked.connect(lambda: self.parent.init_main_menu())
        buttons_layout.addWidget(self.back_button)

        # دکمه ورود
        self.login_button = QPushButton("ورود")
        self.login_button.setFont(QFont('Arial', 14))
        self.login_button.setStyleSheet(button_style + """
            QPushButton {
                background-color: #2ecc71;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.login_button.clicked.connect(self.check_login)
        self.login_button.setDefault(True)
        buttons_layout.addWidget(self.login_button)

        form_layout.addLayout(buttons_layout)

        # دکمه کمک (بازیابی رمز عبور)
        self.help_button = QPushButton("بازیابی رمز عبور")
        self.help_button.setFont(QFont('Arial', 12))
        self.help_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #3498db;
                text-decoration: underline;
                padding: 8px;
                border: none;
            }
            QPushButton:hover {
                color: #2980b9;
            }
        """)
        self.help_button.clicked.connect(self.show_help)
        form_layout.addWidget(self.help_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # افزودن فرم به چیدمان کلی
        fixed_left_layout.addLayout(form_layout)
        outer_layout.addWidget(fixed_left_widget, 0, Qt.AlignmentFlag.AlignCenter)

    # تابع بررسی اطلاعات ورود
    def check_login(self):
        db = DataBase("project_db.db")
        username = self.username.text()
        password = self.password.text()

        try:
            correct_password = db.manager_pass(username)
            if correct_password and correct_password[0] == password:
                QMessageBox.information(self, "موفق", "خوش آمدید", QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.warning(self, "خطا", "نام کاربری یا رمز عبور اشتباه است!", QMessageBox.StandardButton.Ok)
                self.username.setText("")
                self.password.setText("")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا: {str(e)}", QMessageBox.StandardButton.Ok)
            self.username.setText("")
            self.password.setText("")

    # تابع نمایش دیالوگ بازیابی رمز عبور
    def show_help(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("بازیابی رمز عبور")
        dialog.setFixedSize(450, 300)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 15px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # استایل ورودی‌های دیالوگ
        dialog_input_style = """
            QLineEdit {
                font-size: 14px;
                border: 2px solid #dfe6e9;
                border-radius: 8px;
                padding: 12px 15px;
                background-color: #f8f9fa;
                color: #2d3436;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: white;
            }
        """

        # استایل دکمه‌های دیالوگ
        dialog_button_style = """
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                min-width: 120px;
                color: white;
                background-color: #3498db;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """

        # مرحله اول (سؤال امنیتی)
        first_stage = QVBoxLayout()
        first_stage.setSpacing(15)

        label = QLabel("تاریخ تولد شما چیست؟")
        label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        label.setStyleSheet("color: #2c3e50;")
        first_stage.addWidget(label)

        username_edit = QLineEdit()
        username_edit.setPlaceholderText("نام کاربری")
        username_edit.setFont(QFont('Arial', 12))
        username_edit.setStyleSheet(dialog_input_style)
        first_stage.addWidget(username_edit)

        answer_edit = QLineEdit()
        answer_edit.setPlaceholderText("جواب")
        answer_edit.setFont(QFont('Arial', 12))
        answer_edit.setStyleSheet(dialog_input_style)
        first_stage.addWidget(answer_edit)

        verify_button = QPushButton("تایید")
        verify_button.setFont(QFont('Arial', 12))
        verify_button.setStyleSheet(dialog_button_style)
        first_stage.addWidget(verify_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # مرحله دوم (تغییر رمز عبور)
        second_stage = QVBoxLayout()
        second_stage.setSpacing(15)

        new_pass_label = QLabel("رمز عبور جدید:")
        new_pass_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        new_pass_label.setStyleSheet("color: #2c3e50;")
        second_stage.addWidget(new_pass_label)

        new_pass_edit = QLineEdit()
        new_pass_edit.setPlaceholderText("رمز جدید")
        new_pass_edit.setFont(QFont('Arial', 12))
        new_pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        new_pass_edit.setStyleSheet(dialog_input_style)
        second_stage.addWidget(new_pass_edit)

        confirm_pass_edit = QLineEdit()
        confirm_pass_edit.setPlaceholderText("تایید رمز عبور")
        confirm_pass_edit.setFont(QFont('Arial', 12))
        confirm_pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        confirm_pass_edit.setStyleSheet(dialog_input_style)
        second_stage.addWidget(confirm_pass_edit)

        submit_button = QPushButton("تغییر رمز عبور")
        submit_button.setFont(QFont('Arial', 12))
        submit_button.setStyleSheet(dialog_button_style)
        second_stage.addWidget(submit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # ساخت ویجت‌ها برای مراحل
        first_widget = QWidget()
        first_widget.setLayout(first_stage)
        second_widget = QWidget()
        second_widget.setLayout(second_stage)
        second_widget.hide()  # مرحله دوم در ابتدا پنهان است

        main_layout.addWidget(first_widget)
        main_layout.addWidget(second_widget)
        dialog.setLayout(main_layout)

        # تابع بررسی پاسخ به سؤال امنیتی
        def verify_answer():
            db = DataBase("project_db.db")
            answer = db.manager_recovery(username_edit.text())
            if answer and answer[0] == answer_edit.text():
                first_widget.hide()
                second_widget.show()
            else:
                QMessageBox.warning(dialog, "خطا", "نام کاربری یا رمز عبور اشتباه است!", QMessageBox.StandardButton.Ok)
                username_edit.setText("")
                answer_edit.setText("")

        # تابع ثبت رمز عبور جدید
        def submit_new_password():
            new_pass = new_pass_edit.text()
            confirm_pass = confirm_pass_edit.text()

            if not new_pass:
                QMessageBox.warning(dialog, "خطا", "رمز عبور جدید را وارد کنیم", QMessageBox.StandardButton.Ok)
                return

            if new_pass != confirm_pass:
                QMessageBox.warning(dialog, "خطا", "رمز عبور تطابق ندارد", QMessageBox.StandardButton.Ok)
                return

            try:
                db = DataBase("project_db.db")
                db.update_pass(username_edit.text(), new_pass)
                QMessageBox.information(dialog, "موفق", "رمز عبور با موفقیت تغییر یافت",
                                        QMessageBox.StandardButton.Ok)
                dialog.accept()
            except Exception as e:
                QMessageBox.critical(dialog, "خطا", f"رمز عبور تغییر نیافت: {str(e)}",
                                     QMessageBox.StandardButton.Ok)

        # اتصال رویدادها به توابع
        verify_button.clicked.connect(verify_answer)
        answer_edit.returnPressed.connect(verify_answer)
        submit_button.clicked.connect(submit_new_password)
        new_pass_edit.returnPressed.connect(submit_new_password)
        confirm_pass_edit.returnPressed.connect(submit_new_password)

        # نمایش دیالوگ
        dialog.exec()
