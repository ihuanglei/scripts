#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hl_email import email

from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
  
@email('smtp.ym.163.com', 'data@renrenbx.com', 'yunying', 'data@renrenbx.com', 'leihuang@renrenbx.com')
def test_email(content):
  msg = MIMEText(content, 'plain', 'utf-8')
  msg['From'] = Header(u'来自测试的我', 'utf-8')
  msg['To'] =  Header(u'给测试的你', 'utf-8')
  msg['Subject'] = Header(u'自动测试', 'utf-8').encode()
  return msg

@email('smtp.ym.163.com', 'data@renrenbx.com', 'yunying', 'data@renrenbx.com', 'leihuang@renrenbx.com')  
def test_attachment(content, file):
  msg = MIMEMultipart('alternative')
  msg['Subject'] = Header(u'附件测试', 'utf-8').encode()
  msg['From'] = Header(u'来自测试的我', 'utf-8')
  msg['To'] =  Header(u'给测试的你', 'utf-8')
  msg.attach(MIMEText(content, 'plain', 'utf-8'))
  
  att = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
  att["Content-Type"] = 'application/octet-stream'    
  att["Content-Disposition"] = 'attachment; filename="%s"' % Header(u'测试文件.pdf', 'utf-8').encode()
  msg.attach(att)
  
  return msg
  
  
#test_attachment('111','test.pdf')

print reduce(lambda x, y: x+y, [1, 2, 3, 4, 5], 10)

a = 10

print 'fadsf' if a > 11 else 'aa'

