import pandas as pd
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *

def insert_url(text):
    if 'data.go.kr' in text:
        url = text
        try:
            html = urlopen(url)

            bsObject = BeautifulSoup(html, "html.parser")

            primary_key = url
            primary_key = primary_key.split("data/")[1].strip()
            primary_key = primary_key.split("/")[0].strip()

            tables = bsObject.select('table')
            table_html = str(tables)
            table_df_list = pd.read_html(table_html)
            table_df = table_df_list[0]
            return primary_key, table_df, bsObject

        except HTTPError as err:
            msg = QMessageBox()
            msg.setWindowTitle('경고')
            msg.setText('페이지를 찾을 수 없습니다!')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return 0, 0, 0

    else:
        msg = QMessageBox()
        msg.setWindowTitle('경고')
        msg.setText('올바른 공공데이터포털 파일데이터 주소를 입력해주세요')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return 0, 0, 0
