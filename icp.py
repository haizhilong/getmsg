#!/usr/bin/python
#coding: utf-8

import requests
from bs4 import BeautifulSoup

class Icp(object):
	"""docstring for Icp"""
	def __init__(self, domain):
		self.domain=domain

	@property
	def response(self):
		try:
			return requests.get("http://icp.chinaz.com/"+self.domain,allow_redirects=False,timeout=1)
		except:
			pass

	@property
	def soup(self):
		if self.response.content:
			return BeautifulSoup(self.response.content,'lxml')

	@property
	def detail(self):
		try:
			temp=self.soup.find_all("li",class_='clearfix')
			infos=[]
			for x in temp:
				infos.append(x.get_text())
			info={}
			info['name']=infos[0].replace(u'主办单位名称','').replace(u"使用高级查询纠正信息",'')
			info['property']=infos[1].replace(u'主办单位性质','')
			info['num']=infos[2].replace(u'网站备案/许可证号','').replace(u"查看截图",'')
			info['sitename']=infos[3].replace(u'网站名称','')
			info['indexpage']=infos[4].replace(u'网站首页网址','')
			info['checktime']=infos[6].replace(u'审核时间','')
			return info
		except:
			pass

if __name__ == '__main__':
	me=Icp('reading-china.com')
	print(me.detail)
