#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import functools

import smtplib

def send(smtp_server, username, password, sender, receiver, msg):
  smtp = smtplib.SMTP()
  smtp.connect(smtp_server)
  smtp.login(username, password)
  smtp.sendmail(sender, receiver, msg.as_string())
  smtp.quit()
  
def email(smtp_server, username, password, sender, receiver):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      msg = func(*args, **kwargs)
      send(smtp_server, username, password, sender, receiver, msg)
    return wrapper
  return decorator