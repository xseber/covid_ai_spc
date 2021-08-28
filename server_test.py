# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 22:07:20 2020

@author: xseber
"""

import requests
url = 'https://covid19-test-a70c0.uc.r.appspot.com/api'
#url = 'http://127.0.0.1:5000/api'
json = {'questionId':'a105', 'answer':'ปวดครับ', 'dataType': 'String'}
s = requests.post(url, json= json)
print(s.text)