from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
	url = 'http://www.27270.com/tag/649.html'
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
	req = requests.get(url=url, headers=headers)
	req = requests.get(url=url, headers=headers)
	req.encoding = 'gb2312'
	html = req.text
	bf = BeautifulSoup(html, 'lxml')
	targets_url = bf.find('div', class_='w1200 oh').find_all('a', target='_blank')
	for each in targets_url:
		img_req = requests.get(url=each.get('href'), headers=headers)
		img_req.encoding = 'gb2312'
		html = img_req.text
		bf = BeautifulSoup(html, 'lxml')
		img_url = bf.find('div', class_='articleV4Body').find('img')['src']
		name = each.img.get('alt') + '.jpg'
		path = r'./新建文件夹'
		file_name = path + '\\' + name
		try:
			req1 = requests.get(img_url, headers=headers)
			f = open(file_name, 'wb')
			f.write(req1.content)
			f.close()
		except:
			print("some error")

