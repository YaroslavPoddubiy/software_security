from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox


MODES = {
    "ECB": DES.MODE_ECB,
    "CBC": DES.MODE_CBC,
    "CFB": DES.MODE_CFB,
    "OFB": DES.MODE_OFB,
}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("uis/MainWindow.ui", self)

        self.file_name = ""

        self.setWindowTitle('Шифрування DES')

        self.choose_file_button.clicked.connect(self.choose_file)

        self.__set_modes()

        self.encrypt_button.clicked.connect(lambda: self.debug(self.encrypt))
        self.decrypt_button.clicked.connect(lambda: self.debug(self.decrypt))

        self.save_button.clicked.connect(lambda: self.debug(self.save))
        self.save_as_button.clicked.connect(lambda: self.debug(self.save_as))

        self.developer_info_button.clicked.connect(lambda: self.debug(self.developer_info))

    def __set_modes(self):
        for mode in MODES:
            self.mode.addItem(mode)

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
        mode = MODES[self.mode.currentText()]
        key = self.key.text().encode('Windows-1251')
        text = self.textEdit.toPlainText().encode('Windows-1251')
        if mode != DES.MODE_ECB:
            iv = os.urandom(8)
            cipher = DES.new(key, mode, iv)
            ciphertext = iv + cipher.encrypt(pad(text, DES.block_size))
        else:
            cipher = DES.new(key, mode)
            ciphertext = cipher.encrypt(pad(text, DES.block_size))

        self.textEdit.setText(ciphertext.decode('Windows-1251'))

    def decrypt(self):
        mode = MODES[self.mode.currentText()]
        key = self.key.text().encode('Windows-1251')
        text = self.textEdit.toPlainText().encode('Windows-1251')
        if mode != DES.MODE_ECB:
            iv = text[:8]
            ciphertext = text[8:]
            cipher = DES.new(key, mode, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)
        else:
            cipher = DES.new(key, mode)
            plaintext = unpad(cipher.decrypt(text), DES.block_size)

        self.textEdit.setText(plaintext.decode('Windows-1251'))

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
