from bs4 import BeautifulSoup
import base64
import requests

class Parser:
    #data-ri : count로 count번째 이미지 검색 파일이 없을 경우 -1하여 scroll down
    def result_image_page(self, html_source, count):
        try:
            bs = BeautifulSoup(html_source, 'html.parser')
            link = bs.find("div", {"data-ri": str(count)}).find('a')['href']

            return link
        except AttributeError as e:
            print(e)

            return -1

    #image를 가진 url(src)리턴
    def get_image_url(self, html_source):
        bs = BeautifulSoup(html_source, 'html.parser')

        list = bs.findAll('a', {"tabindex": '0'})
        for link in list:
            img_link = link.find('img', {'class': 'irc_mut'})
            if img_link is not None:
                return img_link['src']

        return None

    #url으로 파일 포맷을 지정하여 저장함
    @staticmethod
    def download_image(url):
        if url.startswith('data'):
            data = url.split(',', 1)
            head, data = data[0], data[1]

            data = base64.b64decode(data)
            file_format = head[head.find('/')+1: head.find(';')]
            if not file_format.startswith('.'):
                file_format = '.' + file_format
        else:
            file_format = url.split('.')[-1]
            data = requests.get(url)

        if len(file_format) > 5:
            file_format = '.jpg'

        return data, file_format
