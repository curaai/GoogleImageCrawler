from crawling import crawler

print('구글에서 다운받고 싶은 이미지를 입력해주세요')
keyword = input("입력 : ")
count = int(input("이미지의 개수 : "))

temp = crawler.Crawler(keyword, count)
temp.crawling()