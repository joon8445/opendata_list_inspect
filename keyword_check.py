
def keyword_check(table_df):
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
        return '적합'
    else:
        result_3 = '키워드 NULL ' + result_3_1
        result_3+= '\n동일 키워드 ' + result_3_2
        return result_3

