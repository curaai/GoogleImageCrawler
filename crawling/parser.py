from bs4 import BeautifulSoup

class Parser:
    def result_image_page(self, html_source, count):
        bs = BeautifulSoup(html_source, 'html.parser')
        link = bs.find("div", {"data-ri": str(count)}).find('a')['href']

        # data-ri : count 가 없을 경우 스크롤하여 데이터를 추가함
        if not link:
            return -1

        return link

    def get_image_url(self, html_source, tag):
        bs = BeautifulSoup(html_source, 'html.parser')

        for line in bs.findAll('img', {"class": tag}):
            try:
                if line['height']:
                    return line['src']
            except KeyError as e:
                continue
        return None
