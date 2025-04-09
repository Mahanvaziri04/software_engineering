from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QLabel, QVBoxLayout
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QPalette, QBrush
from PyQt6.QtCore import Qt
from manager_login import ManagerLogin
from staff_login import StaffLogin


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("گیم نت")
        self.setWindowIcon(QIcon("logo.png"))
        self.setGeometry(300, 200, 1000, 600)

        # Set background image
        self.set_background("main.jpg")
        self.init_main_menu()

    def set_background(self, image_path):
        """Sets a background image that scales with the window"""
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

    def resizeEvent(self, event):
        """Handle window resize events to update the background"""
        self.set_background("main.jpg")
        super().resizeEvent(event)

    def init_main_menu(self):
        """Creates the main menu interface with Manager and Staff buttons."""
        self.clear_layout()

        # Create a central widget with transparent background
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)

        # Main layout with proper spacing
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 100)  # Add bottom margin
        layout.setSpacing(30)

        # Add top spacer
        layout.addStretch(2)

        # Button container for better centering
        button_container = QWidget()
        button_container.setStyleSheet("background: transparent;")
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Common button style
        button_style = """
            QPushButton {
                background-color: rgba(74, 110, 155, 0.9);
                border: none;
                border-radius: 25px;
                color: white;
                font-weight: bold;
                min-width: 175px;  /* Reduced from 300px */
                min-height: 40px;  /* Reduced from 70px */
                padding: 14px 28px;  /* Slightly reduced */
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

        # Staff Button
        self.staff_button = QPushButton("کارکن", button_container)
        self.staff_button.setFont(QFont('nazanintar', 18, QFont.Weight.Bold))
        self.staff_button.setStyleSheet(button_style)
        self.staff_button.clicked.connect(self.show_staff_login)
        button_layout.addWidget(self.staff_button, 0, Qt.AlignmentFlag.AlignCenter)

        # Manager Button
        self.manager_button = QPushButton("مالک", button_container)
        self.manager_button.setFont(QFont('nazanintar', 18, QFont.Weight.Bold))
        self.manager_button.setStyleSheet(button_style.replace("rgba(74, 110, 155, 0.9)", "rgba(46, 125, 50, 0.9)")
                                          .replace("rgba(111, 134, 161, 0.9)", "rgba(69, 155, 73, 0.9)")
                                          .replace("rgba(58, 91, 159, 0.9)", "rgba(35, 105, 39, 0.9)"))
        self.manager_button.clicked.connect(self.show_manager_login)
        button_layout.addWidget(self.manager_button, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(button_container, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(0)

    def clear_layout(self):
        """Removes all widgets before switching screens."""
        for widget in self.findChildren(QPushButton):
            widget.deleteLater()
        for widget in self.findChildren(QLineEdit):
            widget.deleteLater()
        for widget in self.findChildren(QLabel):
            widget.deleteLater()

    def show_manager_login(self):
        self.clear_layout()
        self.manager_login = ManagerLogin(self)
        self.setCentralWidget(self.manager_login)

    def show_staff_login(self):
        self.clear_layout()
        self.staff_login = StaffLogin(self)
        self.setCentralWidget(self.staff_login)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()