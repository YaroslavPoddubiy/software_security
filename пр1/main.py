from caesar_cipher import CaesarCipher
import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("uis/MainWindow.ui", self)

        self.caesar_cipher = CaesarCipher()
        self.file_name = ""

        self.setWindowTitle('Шифр Цезаря')

        self.choose_file_button.clicked.connect(self.choose_file)

        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)

        self.save_button.clicked.connect(self.save)
        self.save_as_button.clicked.connect(self.save_as)

        self.developer_info_button.clicked.connect(self.developer_info)

    def load_file_data(self, fname):
        with open(fname, 'r') as f:
            text = f.read()
            self.textEdit.setText(text)

    def choose_file(self):
        fname = QFileDialog(self).getOpenFileName(self, 'Open file',
                                                  os.path.dirname(os.path.abspath(__file__)), "Text files (*.txt)")
        if fname[0]:
            self.load_file_data(fname[0])
            self.file_name = fname[0]

    def encrypt(self):
        try:
            encrypted_text = self.caesar_cipher.encrypt(self.textEdit.toPlainText(), self.keyLineEdit.text())
            self.textEdit.setText(encrypted_text)
        except Exception as ex:
            error_window = QMessageBox(text=str(ex))
            error_window.setWindowTitle("Помилка")
            error_window.setIcon(QMessageBox.Warning)
            error_window.exec_()

    def decrypt(self):
        try:
            decrypted_text = self.caesar_cipher.decrypt(self.textEdit.toPlainText(), self.keyLineEdit.text())
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
