import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import wget


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
        self.Url.clear()

    def btn_1_function(self):

        self.progress=0
        self.progressBar.setValue(self.progress)

        text = self.Url.text()
        self.reset_function()
        self.insert_url(text)

    def test(self, text):
        print(text+'!')


    def insert_url(self, text):

        if 'data.go.kr' in text:
            url = text
            html = urlopen(url)
            bsObject = BeautifulSoup(html, "html.parser")

            primary_key = url
            primary_key = primary_key.split("data/")[1].strip()
            primary_key = primary_key.split("/")[0].strip()

            tables = bsObject.select('table')
            table_html = str(tables)
            table_df_list = pd.read_html(table_html)
            table_df = table_df_list[0]
            self.progress += 1
            self.progressBar.setValue(self.progress)

            try:
                title_data = bsObject.find('div', class_='title')
                file_title = title_data.get_text()
            except AttributeError as err:
                title_data = bsObject.find('p', class_='tit file-data-title')
                file_title = title_data.get_text()

            corp = table_df[1:2][3][1]

            # 기관명 누락
            if file_title.startswith(corp):
                result_1_1 = '적합'
            else:
                result_1_1 = '오류 : 기관명 누락:\n' + file_title

            # 등록주기 포함함
            update_cycle = table_df[:][1][4]
            if '수시' in update_cycle:
                result_1_2 = '적합'
            else:
                if (
                        '월간' in file_title or '연간' in 'file_title' or '수시' in file_title or '분기' in file_title or '년간' in file_title or 'API' in file_title or file_title.endswith(
                        '_')):
                    result_1_2 = '오류 : \n업데이트 주기가 \'수시\'가 아니면서 (일간,월간,분기,년간) 목록명에 일자,월,년도 형태(YYYYMMDD, YYYYMM, YYYY 등)의 내용이 포함되면 오류'
                    result_1_2 += '\n: ' + file_title
                else:
                    result_1_2 = '적합'

            # 숫자4개이상 포함
            if '수시' in update_cycle:
                result_1_2_1 = '적합'
            else:
                count = 0
                for chr in file_title:
                    if chr.isdigit():
                        count += 1
                        print(count)

                if count > 3:
                    result_1_2_1 = '(숫자4개이상 포함) 직접확인하세요 \n오류  : 업데이트 주기가 \'수시\'가 아니면서 (일간,월간,분기,년간) 목록명에 일자,월,년도 형태(YYYYMMDD, YYYYMM, YYYY 등)의 내용이 포함되면 오류'
                    result_1_2_1 += '\n: ' + file_title
                else:
                    result_1_2_1 = '적합'

            repeat = pd.read_excel('./중복오류.xlsx')


            # 동일기관 목록명 중복
            if repeat['공공데이터_기본키'].isin([primary_key]).any():
                result_1_3 = '오류'
                is_repeat = repeat['공공데이터_제목'] == file_title
                repeat_df = repeat[is_repeat]
                count = np.array(repeat_df['중복개수'].values[0])
                result_1_3 = '오류 : \n' + str(count) + '건의 목록명이 중복됨:'
                try:
                    for i in range(int(count)):
                        result_1_3 += '\n' + str(np.array(repeat_df['공공데이터_기본키'].values[i]))
                        result_1_3 += str(np.array(repeat_df['공공데이터_제목'].values[i]))

                except:
                    result_1_3 += '\n 실행오류! 직접 확인하세요!'

            else:
                result_1_3 = '적합'
            self.progress += 1
            self.progressBar.setValue(self.progress)


            # display
            if result_1_1 == result_1_2 == result_1_2_1 == result_1_3 == '적합':
                self.result_1.append('모두 적합')
            else:
                self.result_1.append('기관명 누락 ' + result_1_1)
                self.result_1.append('기관명 누락 ' + result_1_1)
                self.result_1.append('등록주기포함 ' + result_1_2)
                self.result_1.append('등록주기포함(날짜) ' + result_1_2_1)
                self.result_1.append('동일기관 목록명중복 ' + result_1_3)


            # BRM 분류체계
            self.progress += 1
            self.progressBar.setValue(self.progress)

            self.result_2.append('적합')

            # 키워드 NULL
            keword = table_df[:][3][7]
            keyword_list = keword.split(',')
            if len(keyword_list):
                result_3_1 = '적합'
            else:
                result_3_1 = '오류 : 키워드가 누락되었음'

            # 동일 키워드
            keyword_set = set(keyword_list)
            if len(keyword_set) == len(keyword_list):
                result_3_2 = '적합'
            else:
                result_3_2 = '오류 : ' + str(len(keyword_list) - len(keyword_set) + 1) + '건의 키워드가 동일함'


            if result_3_1 == result_3_2 == '적합':
                self.result_3.append('전부 적합')
            else:
                self.result_3.append('키워드 NULL ' + result_3_1)
                self.result_3.append('동일 키워드 ' + result_3_2)

            self.progress += 1
            self.progressBar.setValue(self.progress)




            # 첨부파일 확장자
            file_extension = table_df[:][1][6]
            result_5 = '오류'
            spans = bsObject.find_all('span')
            for span in spans:
                if file_extension in span.text:
                    result_5 = '적합'
                    scripts = bsObject.find_all('script')
                    for script in scripts:
                        if 'encodingFormat' in script.text:
                            file_format = script.text.strip()
                            file_format = file_format.split("encodingFormat\":\"")[1].strip()
                            file_format = file_format.split("\"")[0].strip()
                            if file_format != file_extension:
                                result_5 = '오류'
            # 첨부파일 확장자
            provide = table_df[:][1][9]
            if provide.startswith('기관자체'):
                result_5 = '직접확인 (바로가기)'
            if result_5 == '적합':
                scripts = bsObject.find_all('script')
                for script in scripts:
                    if 'contentUrl' in script.text:
                        contentUrl = script.text.strip()
                        contentUrl = contentUrl.split("contentUrl\": \"")[1].strip()
                        contentUrl = contentUrl.split("\"")[0].strip()
                try:
                    ans = wget.download(contentUrl, out="./data")
                except Exception as err:
                    # stop(err)
                    ans = wget.download(contentUrl)

                ansList = ans.split(".")
                extend = ansList[-1]
                if file_extension.lower() == extend:
                    result_5 = '적합'
                elif extend == 'zip':
                    result_5 = '적합(zip)'
                else:
                    result_5 = '오류 : 첨부파일의 확장자가 잘못 등록되었음\n' + file_extension + ' -> ' + extend + '로 수정 요망'


            self.progress += 1
            self.progressBar.setValue(self.progress)

            self.result_5.append(result_5)

            # 실 데이터 건수 확인
            # # provide = table_df[:][1][9]
            # # if provide.startswith('기관자체'):
            # #     result_7 = '직접확인 (바로가기)'
            # #     result_6 = '적합 (바로가기)'
            # # elif extend == 'csv':
            # #     if 'data.go.kr' in contentUrl:
            # #         try:
            # #             if file_extension == 'CSV':
            # #                 df = pd.read_csv(contentUrl, encoding='cp949')
            # #                 if table_df[:][3][5] == str(len(df)):
            # #                     result_6 = '적합'
            # #                 else:
            # #                     result_6 = '오류 : \n데이터의 실 건수가 타이틀을 제외하고 ' + str(len(df)) + "건임\n"
            # #                     result_6 += str(table_df[:][3][5]) + " -> " + str(len(df)) + ' 수정 요망'
            # #             elif file_extension == 'HWP':
            # #                 result_6 = '적합 (HWP)'
            # #             elif file_extension == 'PDF':
            # #                 result_6 = '적합 (HWP)'
            # #             else:
            # #                 result_6 = 'CSV아님 직접확인'
            # #         except UnicodeDecodeError:
            # #             if file_extension == 'CSV':
            # #                 df = pd.read_csv(contentUrl)
            # #                 if table_df[:][3][5] <= str(len(df))+1 and table_df[:][3][5] >= str(len(df))-1:
            # #                     result_6 = '적합'
            # #                 else:
            # #                     result_6 = '오류 : \n데이터의 실 건수가 타이틀을 제외하고 ' + str(len(df)) + "건임\n"
            # #                     result_6 += str(table_df[:][3][5]) + " -> " + str(len(df)) + ' 수정 요망'
            # #             else:
            # #                 result_6 = 'CSV아님 직접확인'
            #     #         elif(file_extension=='XLSX'):
            #     #             df = pd.read_excel(contentUrl)
            #     #             #df = pd.read_csv(contentUrl)
            #     #             if(table_df[:][3][5]==str(len(df))):
            #     #                 result_6='적합 (엑셀파일 확인)'
            #     #             else:
            #     #                 result_6= '오류 : \n데이터의 실 건수가 타이틀을 제외하고 '+str(len(df))+"건임\n"
            #     #                 result_6+= str(table_df[:][3][5])+ " -> " + str(len(df)) +' 수정 요망'
            # 
            #     else:
            #         result_6 = 'CSV아님 직접확인'
            # else:
            #     result_6 = 'CSV아님 직접확인'
            result_4='적합'
            self.progress += 1
            self.progressBar.setValue(self.progress)
            self.result_4.append(result_4)









        else:
            msg = QMessageBox()
            msg.setWindowTitle('경고')
            msg.setText('올바른 공공데이터포털 파일데이터 주소를 입력해주세요')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()



if __name__== "__main__" :
    app = QApplication(sys.argv)

    myWindow = WindowClass()

    myWindow.show()

    app.exec_()