from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QMessageBox, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from data_base import DataBase


class StaffLogin(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        # Main container styling
        self.setStyleSheet("""
            background-color: #f5f7fa;
        """)

        outer_layout = QHBoxLayout(self)
        fixed_left_widget = QWidget()
        fixed_left_widget.setFixedSize(450, 500)
        fixed_left_widget.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
            padding: 30px;
            border: 1px solid #e0e0e0;
        """)

        fixed_left_layout = QVBoxLayout(fixed_left_widget)
        fixed_left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fixed_left_layout.setSpacing(25)

        # Title label (Persian)
        self.label = QLabel("ورود کارکنان")
        self.label.setFont(QFont('nazanintar', 24, QFont.Weight.Bold))
        self.label.setStyleSheet("""
            color: #2c3e50;
            padding-bottom: 10px;
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fixed_left_layout.addWidget(self.label)

        # Input field style
        input_style = """
            QLineEdit {
                font-size: 14px;
                border: 2px solid #dfe6e9;
                border-radius: 8px;
                padding: 12px 15px;
                min-width: 250px;
                background-color: #f8f9fa;
                color: #2d3436;
                text-align: right;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                background-color: white;
            }
            QLineEdit:hover {
                border: 2px solid #b2bec3;
            }
        """

        # Form layout
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        # Username field (Persian)
        self.username = QLineEdit()
        self.username.setFont(QFont('nazanintar', 14))
        self.username.setPlaceholderText("نام کاربری")
        self.username.setStyleSheet(input_style)
        form_layout.addWidget(self.username)

        # Password field (Persian)
        self.password = QLineEdit()
        self.password.setFont(QFont('nazanintar', 14))
        self.password.setPlaceholderText("رمز عبور")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet(input_style)
        self.password.returnPressed.connect(self.check_login)
        form_layout.addWidget(self.password)

        # Button style
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

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        # Back button (Persian)
        self.back_button = QPushButton("بازگشت")
        self.back_button.setFont(QFont('nazanintar', 14))
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

        # Login button (Persian)
        self.login_button = QPushButton("ورود")
        self.login_button.setFont(QFont('nazanintar', 14))
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
        fixed_left_layout.addLayout(form_layout)

        # Add a subtle footer (Persian)
        footer_label = QLabel("برای مشکلات حساب کاربری با مدیر تماس بگیرید")
        footer_label.setFont(QFont('nazanintar', 10))
        footer_label.setStyleSheet("color: #7f8c8d;")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fixed_left_layout.addWidget(footer_label)

        outer_layout.addWidget(fixed_left_widget, 0, Qt.AlignmentFlag.AlignCenter)

    def check_login(self):
        db = DataBase("project_db.db")
        username = self.username.text()
        password = self.password.text()

        try:
            correct_password = db.staff_pass(username)
            if correct_password and correct_password[0] == password:
                QMessageBox.information(self, "موفقیت", "ورود موفقیت آمیز بود", QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.warning(self, "خطا", "نام کاربری یا رمز عبور نامعتبر است", QMessageBox.StandardButton.Ok)
                self.username.setText("")
                self.password.setText("")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطای سیستم: {str(e)}", QMessageBox.StandardButton.Ok)
            self.username.setText("")
            self.password.setText("")