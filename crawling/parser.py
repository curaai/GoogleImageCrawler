from bs4 import BeautifulSoup


class Parser:
    #data-ri : count로 count번째 이미지 검색 파일이 없을 경우 -1하여 scroll down
    def result_image_page(self, html_source, count):
        bs = BeautifulSoup(html_source, 'html.parser')
        link = bs.find("div", {"data-ri": str(count)}).find('a')['href']

        if not link:
            return -1

        return link

    #image를 가진 url(src)리턴
    def get_image_url(self, html_source, tag):
        bs = BeautifulSoup(html_source, 'html.parser')

        for line in bs.findAll('img', {"class": tag}):
            try:
                if len(line['class']) == 1:
                    return line['src']
                elif line['height']:
                    return line['src']

            except KeyError as e:
                continue

        return None
