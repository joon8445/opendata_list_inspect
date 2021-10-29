import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


from insert_url import insert_url
from brm_check import BRM_check
from title_check import title_check
from keyword_check import keyword_check
from extend_check import extend_check
from data_count_check import data_count_check

form_class = uic.loadUiType("test.ui")[0]

class WindowClass(QMainWindow, form_class):
    progress=0
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.progressBar.setMaximum(6)
        self.Url.returnPressed.connect(self.btn_1_function)
        self.btn_1.clicked.connect(self.btn_1_function)
        self.reset_btn.clicked.connect(self.reset_function)


    def reset_function(self):
        self.result_1.clear()
        self.result_2.clear()
        self.result_3.clear()
        self.result_4.clear()
        self.result_5.clear()
        self.file_title.clear()
        self.Url.clear()
        self.progress = 0
        self.progressBar.setValue(self.progress)

    def btn_1_function(self):
        self.progress=0
        self.progressBar.setValue(self.progress)

        text = self.Url.text()

        self.reset_function()

        primary_key, table_df, bsObject = insert_url(text)
        self.progress += 1
        self.progressBar.setValue(self.progress)
        print(text)
        if (primary_key!= 0):
            file_title, result_1 = title_check(bsObject, primary_key, table_df)
            self.file_title.insert(file_title)
            self.result_1.append(result_1)
            self.progress += 1
            self.progressBar.setValue(self.progress)


            brm_check = BRM_check()
            self.progress += 1
            self.progressBar.setValue(self.progress)
            self.result_2.append(brm_check)

            result_3 = keyword_check(table_df)
            self.result_3.append(result_3)
            self.progress += 1
            self.progressBar.setValue(self.progress)


            result_5 = extend_check(bsObject, table_df)
            self.progress += 1
            self.progressBar.setValue(self.progress)

            self.result_5.append(result_5)
            result_4 = data_count_check()
            self.progress += 1
            self.progressBar.setValue(self.progress)
            self.result_4.append(result_4)
        else:
            self.reset_function()

    def test(self, text):
        print(text+'!')
















if __name__== "__main__" :
    app = QApplication(sys.argv)

    myWindow = WindowClass()

    myWindow.show()

    app.exec_()