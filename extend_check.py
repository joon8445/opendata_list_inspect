import wget
from zipfile import ZipFile
def extend_check(bsObject, table_df):
    # 첨부파일 확장자
    try:
        file_extension = table_df[:][1][6]
        # 첨부파일 확장자
        provide = table_df[:][1][9]
        if provide.startswith('기관자체'):
            result_5 = '직접확인 (바로가기)'
        else:
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
            elif file_extension == extend:
                result_5 = '적합'
            elif extend == 'zip':
                with ZipFile(ans, 'r') as zipObj:
                    listOfFileNames = zipObj.namelist()
                for fileName in listOfFileNames:
                    fileList = fileName.split('.')
                    extend = fileList[-1]
                    if file_extension.lower() == extend:
                        result_5 = '적합'
                        break
                    else:
                        result_5 = '오류 : zip파일 내부에 '+file_extension+'파일이 존재하지 않습니다.'
            else:
                result_5 = '오류 : 첨부파일의 확장자가 잘못 등록되었음\n' + file_extension + ' -> ' + extend + '로 수정 요망'

        return result_5
    except:
        result_5 = '직접 확인하세요'
        return result_5
