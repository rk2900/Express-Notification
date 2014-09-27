#!/usr/bin/env python
# -*- coding: utf8 -*-

import httplib2 as hl
import urllib
from bs4 import BeautifulSoup as bs
import smtplib  
from email.mime.text import MIMEText
import time
import ConfigParser

class Machine:
	def __init__(self):
		self.cookie = None # ''
		self.state = None
		self.response = None
		self.content = None
		self.config = ConfigParser.ConfigParser()
		self.config.read("./settings.config")
		self.bong_user = self.config.get("bong", "username")
		self.bong_pwd = self.config.get("bong", "password")
		self.email_user = self.config.get("email", "username")
		self.email_pwd = self.config.get("email", "password")
		self.email_from = self.config.get("email", "fromAddr")
		self.email_to = self.config.get("email", "toAddr")

	def GetCookie(self):
		print self.cookie
		url = 'https://shop.bong.cn/shop/user/login'
		body = {'password': self.bong_pwd, 'loginName': self.bong_user}
		# print body
		headers = {'Content-type':'application/x-www-form-urlencoded; charset=UTF-8', 
					'Accept-Encoding':'gzip,deflate',
					'Connection':'keep-alive',
					'Content-Length':'39',
					'Referer':'https://shop.bong.cn',
					'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.122 Safari/537.36',
					'X-Requested-With':'XMLHttpRequest'}
		h = hl.Http()
		print "Getting new cookie ..."
		while True:
			self.response, self.content = h.request(url,'POST',headers=headers,body=urllib.urlencode(body))
			if self.response.has_key('set-cookie'):
				break
			print 'Not get cookie, try again ...'
		self.cookie = self.response['set-cookie']
		print "Got new cookie. New cookie is " + self.cookie

	def Query(self):
		h = hl.Http()
		url = 'https://shop.bong.cn/shop/user/orders'

		if not self.cookie:
			print "No cookie, get first one."
			self.GetCookie()

		while True:
			headers = {'Cookie':self.cookie}  
			# print headers
			try:
				self.response, self.content = h.request(url, 'GET', headers=headers) 
			except httplib.ResponseNotReady as e:
				print e
			else:
				soup = bs(self.content)
				self.state = soup.find(name='li', attrs={'class':'order-state color-green os-stocking'})
				if not self.state:
					print "Old cookie does not work, get new one."
					self.GetCookie()
				else:
					break			
			# txt =  self.state.text
			# print 'state is ' + state.text # state = soup.find(name='li', attrs={'class':'order-state color-green os-stocking'})
		txt =  self.state.text
		return txt

	def SendMail(self):
	    msg = MIMEText(self.state.text, _subtype='plain', _charset='gb2312')  
	    msg['Subject'] = "Bong status has changed!"
	    msg['From'] = self.email_from
	    msg['To'] = self.email_to
	  
	    smtp = smtplib.SMTP_SSL("smtp.126.com")  
	    smtp.set_debuglevel(4)  
	    smtp.login(self.email_user, self.email_pwd)
	    smtp.sendmail(self.email_from, self.email_to, msg.as_string())  
	    smtp.quit()


count = 0
m = Machine()
origin_text = m.Query()
while True:
	count = count + 1
	print count
	time.sleep(20)
	txt1 = m.Query()
	if txt1 == origin_text:
		print True
	else:
		m.SendMail()
	origin_text = txt1