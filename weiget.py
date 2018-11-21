#!/usr/bin/python
#coding=utf-8

import json
import requests
import time
from bs4 import BeautifulSoup

class ThirdWeight(object):
	# 第三方权重查询
	# 爱站 站长 5118 
	def __init__(self,domain):
		self.today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
		if domain.startswith("http:"):
			self.domain=domain.replace("http://","")
		else:
			self.domain=domain

	@property
	def wgt5118(self):
		wgt={}
		headers={"Content-Type":"application/x-www-form-urlencoded",'Authorization':'A4BF93AED1334AE08DD63111321CA555',}
		payload={'url':self.domain}
		requ=requests.post('http://apis.5118.com/weight',data=payload,headers=headers)
		for x in json.loads(requ.content)['data']['result']:
			wgt[x['type']]=x['weight']
		return {'5118':wgt}

	@property
	def wgtchinaz(self):
		wgt={}
		requ=requests.get("http://seo.chinaz.com/"+self.domain+'/')
		soup=BeautifulSoup(requ.content,'lxml')
		me=soup.select(".ReLImgCenter")
		for x in me:
			try:
				wgt[x.span.string]=x.img['src'][-5:-4:]
			except TypeError:
				pass
		return {'china':wgt}

	@property
	def wgtaizhan(self):
		wgt={}
		requ=requests.get("https://www.aizhan.com/cha/"+self.domain+'/')
		soup=BeautifulSoup(requ.content,'lxml')
		me=soup.select(".cha-infos > .content > .table > tr")[1]
		for x in me.find_all('a'):
			try:
				wgt[x['id']]=x.img['src'][-5:-4:]
			except TypeError:
				pass
		return {'aizhan':wgt}

	@property
	def wgt(self):
		return {self.today:[self.wgt5118,self.wgtchinaz,self.wgtaizhan]}

if __name__ == '__main__':
	xinsiwen=ThirdWeight('http://www.xinsiwen.com')
	print xinsiwen.wgt
