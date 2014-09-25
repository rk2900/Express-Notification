#!/usr/bin/env python
# -*- coding: utf8 -*-

import httplib2 as hl
import urllib
from bs4 import BeautifulSoup as bs
import smtplib  
from email.mime.text import MIMEText
import time
import ConfigParser

# noExpress = u'备货中'
# hasExpress = u'已出库'
# if txt.find(hasExpress) > 0 or txt.find(noExpress) < 0:
# 	print True
# if txt.find(noExpress) > 0:
# 	print False

def Query(username, password):
	url = 'https://shop.bong.cn/shop/user/login'
	body = {'password': username, 'loginName': password}
	# print body
	headers = {'Content-type':'application/x-www-form-urlencoded; charset=UTF-8', 
				'Accept-Encoding':'gzip,deflate',
				'Connection':'keep-alive',
				'Content-Length':'39',
				'Referer':'https://shop.bong.cn',
				'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.122 Safari/537.36',
				'X-Requested-With':'XMLHttpRequest'}
	h = hl.Http()
	response,content = h.request(url,'POST',headers=headers,body=urllib.urlencode(body))
	cookie = response['set-cookie']

	url = 'https://shop.bong.cn/shop/user/orders'
	headers = {'Cookie':cookie}  
	response, content = h.request(url, 'GET', headers=headers) 

	soup = bs(content)
	state = soup.find(name='li', attrs={'class':'order-state color-green os-stocking'})
	txt =  state.text
	return txt

def SendMail(status, username, password, fromAddr, toAddr):
    msg = MIMEText(status,_subtype='plain',_charset='gb2312')  
    msg['Subject']="Bong status has changed!"
    msg['From']=fromAddr
    msg['To']=toAddr
  
    smtp = smtplib.SMTP_SSL("smtp.126.com")  
    smtp.set_debuglevel(4)  
    smtp.login(username, password)#***为密码  
    smtp.sendmail(fromAddr,toAddr,msg.as_string())  
    smtp.quit()



config = ConfigParser.ConfigParser()
config.read("./settings.config")
bong_user = config.get("bong", "username")
bong_pwd = config.get("bong", "password")
email_user = config.get("email", "username")
email_pwd = config.get("email", "password")
email_from = config.get("email", "fromAddr")
email_to = config.get("email", "toAddr")

origin_text = Query(bong_user, bong_pwd)
while True:
	time.sleep(5)
	txt1 = Query(bong_user, bong_pwd)
	if txt1 == origin_text:
		print True
	else:
		print SendMail(txt1, email_user, email_pwd, email_from, email_to)
	origin_text = txt1