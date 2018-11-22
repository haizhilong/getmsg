#!/usr/bin/python
#coding: utf-8
import useragent
import requests
import time
import urllib
import re
from bs4 import BeautifulSoup


class mp(object):
	headers={
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
	'Referrer Policy': 'no-referrer-when-downgrade',
	'Remote Address': '124.192.132.236:443',
	'Cookie':'IPLOC=CN1100; SUID=06204579541C940A000000005BEF7DC1; SUV=1542421954367722; SNUID=AD8BE9D5ABA9D67F7A0DFE21ACE43732; ld=clllllllll2bEcoClllllVssA0UlllllWUUkxkllll9lllll9ylll5@@@@@@@@@@; LSTMV=322%2C537; LCLKINT=7696; ABTEST=4|1542425179|v1; JSESSIONID=aaa6P2cxQIfI-aePrKYBw; weixinIndexVisited=1; sct=17; ppinf=5|1542426469|1543636069|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTUlQTUlOTQlRTYlQjMlQTIlRTUlODQlQkYlRTclODElOUV8Y3J0OjEwOjE1NDI0MjY0Njl8cmVmbmljazozNjolRTUlQTUlOTQlRTYlQjMlQTIlRTUlODQlQkYlRTclODElOUV8dXNlcmlkOjQ0Om85dDJsdUR4RnpSSWlfVzBmYXZzSGpTSVR5NW9Ad2VpeGluLnNvaHUuY29tfA; pprdig=vqkF_7A6MBMW8XyS-rOEEiHQnpSbTDWh8O0bqJaEx1OkmL98DXXfuqjzX1k_qBFPLuu74iDag2dmpKZs_hIp9sGIHUPsywTOsPbT1_C5_D9L9W-2wv8ymVJNIaYSng8GFq-_ntYiNkubQOyXdYu7WXJIoHKadSeAxdkB7bx4oG4; sgid=13-27670897-AVvvj2XJib6kM5zMMvUjdkAw; ppmdig=15424325530000004d864fd70de70aeb86c5bf2d29ca041f'
	}

	def __init__(self,kw='',page=0):
		self.kw=kw
		self.page=page

	def __call__(self):
		for msg in self.msgs:
			show=msg['name']+'\t'+msg['wxh']+'\t'+msg['company']+'\t'+msg['function']
			print(show)

	@property
	def url(self):
		return "https://weixin.sogou.com/weixin?query="+urllib.parse.quote(self.kw)+"&s_from=input&type=1&page={page}&ie=utf8".format(page=self.page)

	@property
	def soup(self):
		content=requests.get(self.url,timeout=2,headers=self.headers).content
		time.sleep(5)
		return BeautifulSoup(content,'lxml')

	@property
	def count(self):
		me=self.soup.find_all('div',class_='mun')[0].get_text()
		return int(re.sub(r"\D", "", me))  

	@property
	def msgs(self):
		info=[x for x in self.soup.select(".news-list2 > li")]
		cache=[]
		for msg in info:
			try:
				me={}
				text=msg.get_text()
				data=[x for x in text.split("\n") if x]
				me['name']=data[0]
				me['wxh']=data[1][4:]
				me['function']=data[4]
				me['company']=data[6]
				cache.append(me)
			except:
				continue
		return cache



def info(kw=''):
	index=mp(kw,page=1)
	index()
	pn=int(index.count/10)+1
	print(kw+'\t'+str(pn))
	data=[]
	data.extend(index.msgs)
	if pn==1:
		return data
	else:
		for x in range(2,pn):
			info=mp(kw=kw,page=x)
			info()
			data.extend(info.msgs)
			with open('test.txt','a') as f:
				for x in info.msgs:
					data.append(x)
					msg=x['name']+'\t'+x['wxh']+'\t'+x['company']+'\t'+x['function']
					f.write(msg+'\n')
					f.flush()
		return data
		

if __name__ == '__main__':
	# print(info(kw='小故事'))
	index=mp(kw='小故事',page=1)
	index()
	print(index.count)
