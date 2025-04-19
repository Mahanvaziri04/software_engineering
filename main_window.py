# وارد کردن ابزارهای مورد نیاز از PyQt6 برای طراحی رابط کاربری
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QPalette, QBrush
from PyQt6.QtCore import Qt
from manager_login import ManagerLogin  # ایمپورت فرم ورود مدیر
from staff_login import StaffLogin      # ایمپورت فرم ورود کارمند
import sys
import os

# تابع برای پیدا کردن مسیر صحیح فایل (در زمان اجرای بسته‌بندی‌شده مثل PyInstaller)
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# کلاس پنجره اصلی برنامه
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("کلینیک")  # عنوان پنجره
        self.setGeometry(300, 200, 1000, 600)  # اندازه و موقعیت اولیه پنجره

        # تنظیم تصویر پس‌زمینه
        self.set_background(resource_path("main.jpg"))
        self.init_main_menu()  # نمایش منوی اصلی

    # تابع برای تنظیم تصویر پس‌زمینه پنجره
    def set_background(self, image_path):
        palette = self.palette()
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: Could not load background image from {image_path}")
            return

        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )))
        self.setPalette(palette)

    # بازنویسی رویداد تغییر اندازه پنجره برای تغییر اندازه تصویر پس‌زمینه
    def resizeEvent(self, event):
        self.set_background("main.jpg")
        super().resizeEvent(event)

    # تابع ایجاد منوی اصلی با دکمه‌های ورود مدیر و کارمند
    def init_main_menu(self):
        self.clear_layout()  # پاک‌سازی ویجت‌ها از قبل

        # ایجاد ویجت مرکزی با پس‌زمینه شفاف
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)

        # چیدمان عمودی برای قرار دادن عناصر
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 100)  # حاشیه پایین
        layout.setSpacing(30)

        layout.addStretch(2)  # فاصله بالا

        # ویجت داخلی برای دکمه‌ها
        button_container = QWidget()
        button_container.setStyleSheet("background: transparent;")
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(20)

        # استایل مشترک برای دکمه‌ها
        button_style = """
            QPushButton {
                background-color: rgba(74, 110, 155, 0.9);
                border: none;
                border-radius: 25px;
                color: white;
                font-weight: bold;
                min-width: 175px;
                min-height: 40px;
                padding: 14px 28px;
                margin: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgba(111, 134, 161, 0.9);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: rgba(58, 91, 159, 0.9);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
                transform: translateY(1px);
            }
        """

        # دکمه ورود کارکن
        self.staff_button = QPushButton("کارکن", button_container)
        self.staff_button.setFont(QFont('nazanintar', 18, QFont.Weight.Bold))
        self.staff_button.setStyleSheet(button_style)
        self.staff_button.clicked.connect(self.show_staff_login)
        button_layout.addWidget(self.staff_button, 0, Qt.AlignmentFlag.AlignCenter)

        # دکمه ورود مدیر
        self.manager_button = QPushButton("مالک", button_container)
        self.manager_button.setFont(QFont('nazanintar', 18, QFont.Weight.Bold))
        self.manager_button.setStyleSheet(button_style.replace("rgba(74, 110, 155, 0.9)", "rgba(46, 125, 50, 0.9)")
                                          .replace("rgba(111, 134, 161, 0.9)", "rgba(69, 155, 73, 0.9)")
                                          .replace("rgba(58, 91, 159, 0.9)", "rgba(35, 105, 39, 0.9)"))
        self.manager_button.clicked.connect(self.show_manager_login)
        button_layout.addWidget(self.manager_button, 0, Qt.AlignmentFlag.AlignCenter)

        # افزودن دکمه‌ها به چیدمان اصلی
        layout.addWidget(button_container, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(0)

    # تابع پاک‌سازی ویجت‌ها از صفحه فعلی
    def clear_layout(self):
        for widget in self.findChildren(QPushButton):
            widget.deleteLater()
        for widget in self.findChildren(QLineEdit):
            widget.deleteLater()
        for widget in self.findChildren(QLabel):
            widget.deleteLater()

    # نمایش فرم ورود مدیر
    def show_manager_login(self):
        self.clear_layout()
        self.manager_login = ManagerLogin(self)
        self.setCentralWidget(self.manager_login)

    # نمایش فرم ورود کارمند
    def show_staff_login(self):
        self.clear_layout()
        self.staff_login = StaffLogin(self)
        self.setCentralWidget(self.staff_login)

# اجرای برنامه
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
