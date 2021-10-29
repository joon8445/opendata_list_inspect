import pandas as pd
import numpy as np

def title_check(bsObject, primary_key, table_df):
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
                '_월간' in file_title or '_연간' in 'file_title' or '_수시' in file_title or '_분기' in file_title or '_년간' in file_title or 'API' in file_title or file_title.endswith(
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

        if count > 3:
            result_1_2_1 = '(숫자4개이상 포함) 직접확인하세요 \n오류  : 업데이트 주기가 \'수시\'가 아니면서 (일간,월간,분기,년간) 목록명에 일자,월,년도 형태(YYYYMMDD, YYYYMM, YYYY 등)의 내용이 포함되면 오류'
            result_1_2_1 += '\n: ' + file_title
        else:
            result_1_2_1 = '적합'

    repeat = pd.read_excel('./중복오류.xlsx')

    # 동일기관 목록명 중복
    if repeat['공공데이터_기본키'].isin([int(primary_key)]).any():
        result_1_3 = '오류'
        is_repeat = repeat['공공데이터_제목'] == file_title
        repeat_df = repeat[is_repeat]
        count = np.array(repeat_df['중복개수'].values[0])
        result_1_3 = '오류 : \n' + str(count) + '건의 목록명이 중복됨:'
        try:
            for i in range(int(count)):
                result_1_3 += '\n' + str(np.array(repeat_df['공공데이터_기본키'].values[i]))
                result_1_3 += ' ' + str(np.array(repeat_df['공공데이터_제목'].values[i]))

        except:
            result_1_3 += '\n 실행오류! 직접 확인하세요!'

    else:
        result_1_3 = '적합'

    # display
    if result_1_1 == result_1_2 == result_1_2_1 == result_1_3 == '적합':
        return file_title, '적합'
    else:
        result_1 = '기관명 누락 ' + result_1_1
        result_1+= '\n등록주기포함 ' + result_1_2
        result_1+= '\n등록주기포함(날짜) ' + result_1_2_1
        result_1+= '\n동일기관 목록명중복 ' + result_1_3

        return file_title, result_1