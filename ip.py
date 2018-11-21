#!/usr/bin/python
#coding: utf-8

import requests

class Ipdetail(object):
	def __init__(self, ip):
		self.taobaourl="http://ip.taobao.com/service/getIpInfo.php?ip="+ip

	@property
	def response(self):
		return requests.get(self.taobaourl,timeout=1)


	@property
	def detail(self):
		return self.response.json()
		

if __name__ == '__main__':
	fip=Ipdetail('202.200.112.06')
	print(fip.detail)
