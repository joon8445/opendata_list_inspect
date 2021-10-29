import wget

def extend_check(bsObject, table_df):
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

        return result_5


