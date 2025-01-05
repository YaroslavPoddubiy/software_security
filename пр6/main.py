import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from RSA import RSACipher


class KeyGenerationWindow(QMainWindow):
    def __init__(self, RSACipher):
        self.__RSACipher = RSACipher
        super(KeyGenerationWindow, self).__init__()
        loadUi("uis/KeyGenerationWindow.ui", self)

        self.generate.clicked.connect(lambda: self.debug(self.__generate_keys))

    @staticmethod
    def debug(function, *args):
        try:
            function(*args)
        except Exception as ex:
            msg = QMessageBox()
            msg.setText(str(ex))
            msg.exec_()

    def __generate_keys(self):
        if self.keyLen.text():
            if int(self.keyLen.text()) < 1:
                raise ValueError("Довжина ключа повинна бути додатньою")
            public_key, private_key = self.__RSACipher.generate_keys(int(self.keyLen.text()))
            self.publicKey.setText(f"{public_key[0]},{public_key[1]}")
            self.privateKey.setText(f"{private_key[0]},{private_key[1]}")
        else:
            public_key, private_key = self.__RSACipher.generate_keys()
            self.publicKey.setText(f"{public_key[0]},{public_key[1]}")
            self.privateKey.setText(f"{private_key[0]},{private_key[1]}")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("uis/MainWindow.ui", self)

        self.file_name = ""

        self.setWindowTitle('Шифрування RSA')

        self.__RSACipher = RSACipher()

        self.choose_file_button.clicked.connect(self.choose_file)

        self.encrypt_button.clicked.connect(lambda: self.debug(self.encrypt))
        self.decrypt_button.clicked.connect(lambda: self.debug(self.decrypt))

        self.keyGenerationButton.clicked.connect(self.show_key_generation_window)

        self.save_button.clicked.connect(lambda: self.debug(self.save))
        self.save_as_button.clicked.connect(lambda: self.debug(self.save_as))

        self.developer_info_button.clicked.connect(lambda: self.debug(self.developer_info))

    def show_key_generation_window(self):
        self.__key_generation_window = KeyGenerationWindow(self.__RSACipher)
        self.__key_generation_window.show()

    def choose_file(self, var_name):
        fname = QFileDialog(self).getOpenFileName(self, 'Open file',
                                                  os.path.dirname(os.path.abspath(__file__)), "Text files (*.txt)")
        if not fname[0]:
            return
        fname = fname[0]

        with open(fname, 'r', encoding="utf-8") as f:
            text = f.read()
            self.textEdit.setText(text)
        self.file_name = fname

    @staticmethod
    def debug(function, *args):
        try:
            function(*args)
        except Exception as ex:
            msg = QMessageBox()
            msg.setText(str(ex))
            msg.exec_()

    def encrypt(self):
        key = (int(num) for num in self.key.text().split(","))
        encrypted_text = self.__RSACipher.encrypt(self.textEdit.toPlainText(), key)

        self.textEdit.setText(encrypted_text)

    def decrypt(self):
        key = (int(num) for num in self.key.text().split(","))
        decrypted_text = self.__RSACipher.decrypt(self.textEdit.toPlainText(), key)

        self.textEdit.setText(decrypted_text)

    def save(self):
        if not self.file_name or not os.path.exists(self.file_name):
            return self.save_as()
        with open(self.file_name, 'w', encoding='utf-8') as f:
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
