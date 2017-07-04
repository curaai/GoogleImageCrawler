import os
import base64


class Controller:
    def __init__(self, path):
        self.path = path

    #이미지 파일 저장
    def save_image(self, data, name, format):
        f = open(self.path + '//' + name + format, 'wb')
        f.write(data)
        f.close()

    #디렉토리 생성
    def makedirectory(self, keyword):
        if not os.path.exists(keyword):
            os.makedirs(keyword)

    #url에 데이터가 있을 경우 url에서 바로 저장
    def save_data_url(self, path, url):
        head, data = url.split(',', 1)
        file_format = head.split(';')[0].split('/')[1]

        data = base64.b64decode(data)
        with open(path + "." + file_format, 'wb') as f:
            f.write(data)