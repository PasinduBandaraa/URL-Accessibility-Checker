import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QLabel
from PySide6.QtCore import Qt  # Import the Qt module

import requests

def check_urls():
    try:
        with open("urls.txt", "r") as file:
            urls = file.read().splitlines()

        results_table.clearContents()
        results_table.setRowCount(len(urls))
        results_table.setColumnCount(2)
        header = ["URL", "Accessibility"]
        results_table.setHorizontalHeaderLabels(header)

        for idx, url in enumerate(urls):
            try:
                response = requests.get(url)
                accessibility = "YES" if response.status_code == 200 else "NO"
                results_table.setItem(idx, 0, QTableWidgetItem(url))
                results_table.setItem(idx, 1, QTableWidgetItem(accessibility))
            except requests.RequestException:
                results_table.setItem(idx, 0, QTableWidgetItem(url))
                results_table.setItem(idx, 1, QTableWidgetItem("NO"))
    except FileNotFoundError:
        results_table.clearContents()
        results_table.setRowCount(1)
        results_table.setColumnCount(1)
        results_table.setItem(0, 0, QTableWidgetItem("urls.txt not found"))

def open_urls_file():
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("Text Files (*.txt)")
    file_dialog.setViewMode(QFileDialog.List)
    file_dialog.setFileMode(QFileDialog.ExistingFiles)
    if file_dialog.exec_():
        file_path = file_dialog.selectedFiles()[0]
        with open(file_path, "r") as file:
            content = file.read()
            # urls_text.setText(content)  # Removed this line

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("URL Accessibility Checker")  # Set application name here
window.setGeometry(100, 100, 500, 400)  # X, Y, Width, Height

# Centered label at the top
label_title = QLabel("URL Accessibility Checker", window)
label_title.setAlignment(Qt.AlignCenter)  # Align the text to center
label_title.setGeometry(50, 10, 400, 30)  # Adjust size as needed
label_title.setStyleSheet("font-size: 18px; font-weight: bold;")

check_button = QPushButton("Check Accessibility", window)
check_button.clicked.connect(check_urls)
check_button.setGeometry(50, 50, 200, 30)
check_button.setStyleSheet("background-color: #4CAF50; color: white;")

open_file_button = QPushButton("Open URLs File", window)
open_file_button.clicked.connect(open_urls_file)
open_file_button.setGeometry(260, 50, 200, 30)

results_table = QTableWidget(window)
results_table.setGeometry(50, 90, 410, 310)
results_table.setColumnCount(2)
results_table.setHorizontalHeaderLabels(["URL", "Accessibility"])

window.show()
sys.exit(app.exec_())
