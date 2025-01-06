import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from RSASignature import RSASignature


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("uis/MainWindow.ui", self)

        self.file_name = ""

        self.message = ""

        self.setWindowTitle('Електронний підпис RSA')

        self.__RSASignature = RSASignature()

        self.choose_file_button.clicked.connect(self.choose_file)

        self.signButton.clicked.connect(lambda: self.debug(self.sign))
        self.verifyButton.clicked.connect(lambda: self.debug(self.verify))

        self.keyGenerationButton.clicked.connect(lambda: self.debug(self.key_generation))

        self.save_button.clicked.connect(lambda: self.debug(self.save))
        self.save_as_button.clicked.connect(lambda: self.debug(self.save_as))

        self.developer_info_button.clicked.connect(lambda: self.debug(self.developer_info))

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

    def key_generation(self):
        try:
            self.__RSASignature.generate_keys()
            message = QMessageBox()
            message.setText("Ключі було збережено у файли 'private_key.pem' і 'public_key.pem'")
            message.exec_()
        except Exception as ex:
            raise ex

    def sign(self):
        if not self.textEdit.toPlainText():
            return
        signed = self.__RSASignature.sign(self.textEdit.toPlainText())
        messageBox = QMessageBox()
        if signed:
            messageBox.setText("Підписано")
            with open('text.txt', 'w') as f:
                f.write(self.textEdit.toPlainText())
        else:
            messageBox.setText("Не вдалося підписати")
        messageBox.exec_()

    def verify(self):
        if not self.textEdit.toPlainText():
            return
        verified = self.__RSASignature.verify(self.textEdit.toPlainText())
        messageBox = QMessageBox()
        if verified:
            messageBox.setText("Підпис верифіковано")
        else:
            messageBox.setText("Підпис не верифіковано")

        messageBox.exec_()

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
