def data_count_check():
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
    result_4 = '적합'
    return result_4