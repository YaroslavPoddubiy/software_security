from book_cipher import BookCipher
import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("uis/MainWindow.ui", self)

        self.book_cipher = BookCipher()
        self.file_name = ""

        self.setWindowTitle('Книжковий шифр')

        self.choose_file_button.clicked.connect(lambda: self.choose_file("textEdit"))
        self.choose_key_button.clicked.connect(lambda: self.choose_file("key"))

        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)

        self.save_button.clicked.connect(self.save)
        self.save_as_button.clicked.connect(self.save_as)

        self.developer_info_button.clicked.connect(self.developer_info)

    def choose_file(self, var_name):
        if var_name not in ("textEdit", "key"):
            return
        fname = QFileDialog(self).getOpenFileName(self, 'Open file',
                                                  os.path.dirname(os.path.abspath(__file__)), "Text files (*.txt)")
        if not fname[0]:
            return
        fname = fname[0]

        with open(fname, 'r', encoding="utf-8") as f:
            text = f.read()
            self.__dict__[var_name].setText(text)
        if var_name == "textEdit":
            self.file_name = fname

    def encrypt(self):
        try:
            encrypted_text = self.book_cipher.encrypt(self.textEdit.toPlainText(), self.key.text())
            self.textEdit.setText(encrypted_text)
        except Exception as ex:
            error_window = QMessageBox(text=str(ex))
            error_window.setWindowTitle("Помилка")
            error_window.setIcon(QMessageBox.Warning)
            error_window.exec_()

    def decrypt(self):
        try:
            decrypted_text = self.book_cipher.decrypt(self.textEdit.toPlainText(), self.key.text())
            self.textEdit.setText(decrypted_text)
        except Exception as ex:
            error_window = QMessageBox(text=str(ex))
            error_window.setWindowTitle("Помилка")
            error_window.setIcon(QMessageBox.Warning)
            error_window.exec_()

    def save(self):
        if not self.file_name or not os.path.exists(self.file_name):
            return self.save_as()
        with open(self.file_name, 'w') as f:
            f.write(self.textEdit.toPlainText())

    def save_as(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files(*);;Text Files(*.txt)")
        if not fname:
            return
        with open(fname, 'x') as f:
            f.write(self.textEdit.toPlainText())
        self.file_name = fname

    def developer_info(self):
        window = QMessageBox(text="Створив студент 4 курсу групи ТВ-13 Поддубій Ярослав")
        window.setWindowTitle("Про розробника")
        window.setIcon(QMessageBox.Information)
        window.exec_()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
