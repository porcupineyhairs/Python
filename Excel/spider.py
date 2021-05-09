import requests
from lxml import html


url = 'https://www.315jiage.cn'

url_search = '/mSearch.aspx'

header = {'Cookie': '__cfduid=ddafd672e26055cee05dc79d2975917491620288856; rtv=54295C,18734053',
           'User-Agent': 'PostmanRuntime/7.26.10'}

def getinfo(name=None):

	data = {'where': 'title', 'keyword': name}

	r = requests.get(url + url_search, params=data, headers=header)

	tree = html.fromstring(r.text)

	scard_list = tree.xpath('//div[@class="badge badge-warning pull-right badge-rounded"]/text()')

	print(scard_list)





if __name__ == '__main__':
	getinfo('6933692547918')
