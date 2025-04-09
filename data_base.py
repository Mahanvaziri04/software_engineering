import sqlite3

class DataBase:
    def __init__(self, name):
        self.name = name

    def manager_pass(self, username):
        """Get password for manager"""
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "SELECT password FROM manager_admin WHERE username = ?",
            (username,)
        )
        password = self.cursor.fetchone()
        self.connect.close()
        return password

    def staff_pass(self, username):
        """Get password for staff"""
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
        """Get security answer for password recovery"""
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
        """Update password (no hashing)"""
        self.connect = sqlite3.connect(self.name)
        self.cursor = self.connect.cursor()
        self.cursor.execute(
            "UPDATE manager_admin SET password = ? WHERE username = ?",
            (new_password, username)
        )
        self.connect.commit()
        self.connect.close()