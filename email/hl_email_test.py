#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hl_email import email

from email.header import Header
from email.mime.text import MIMEText
  
@email('smtp.ym.163.com', 'data@renrenbx.com', 'yunying', 'data@renrenbx.com', 'leihuang@renrenbx.com')
def test_email(content):
  msg = MIMEText(content, 'plain', 'utf-8')
  msg['From'] = Header(u'来自测试的我', 'utf-8')
  msg['To'] =  Header(u'给测试的你', 'utf-8')
  msg['Subject'] = Header(u'自动测试', 'utf-8').encode()
  return msg

  
test_email('111')
