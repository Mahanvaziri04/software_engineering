# ایمپورت کتابخانه‌های مورد نیاز
import sqlite3  # برای ارتباط با پایگاه داده SQLite
import sys
import os

# تابعی برای بازیابی مسیر فایل (در صورتی که فایل اجرایی بسته‌بندی شده باشد مانند PyInstaller)
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# کلاس مدیریت پایگاه داده
class DataBase:
    def __init__(self, name):
        # تعیین مسیر کامل فایل پایگاه داده
        self.name = resource_path(name)

    def manager_pass(self, username):
        """دریافت رمز عبور مدیر با استفاده از نام کاربری"""
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "SELECT password FROM manager_admin WHERE username = ?",
            (username,)
        )
        password = self.cursor.fetchone()  # دریافت اولین نتیجه
        self.connect.close()
        return password

    def staff_pass(self, username):
        """دریافت رمز عبور کارمند با استفاده از نام کاربری"""
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "SELECT password FROM staff WHERE username = ?",
            (username,)
        )
        password = self.cursor.fetchone()
        self.connect.close()
        return password

    def manager_recovery(self, username):
        """دریافت پاسخ امنیتی مدیر برای بازیابی رمز عبور"""
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "SELECT passRecovery FROM manager_admin WHERE username = ?",
            (username,)
        )
        passRecovery = self.cursor.fetchone()
        self.connect.close()
        return passRecovery

    def update_pass(self, username, new_password):
        """بروزرسانی رمز عبور مدیر (بدون رمزنگاری)"""
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "UPDATE manager_admin SET password = ? WHERE username = ?",
            (new_password, username)
        )
        self.connect.commit()  # ثبت تغییرات
        self.connect.close()
