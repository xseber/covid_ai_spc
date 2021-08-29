# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 22:07:20 2020

@author: xseber
"""

import requests
from timeit import default_timer as timer
from datetime import timedelta
start =  timer()

#url = 'https://covid19-test-a70c0.uc.r.appspot.com/api'
url = 'http://127.0.0.1:5000/check_word'
json = {'questionId':'a105', 'answer':'ใช่', 'dataType': 'String'}
s = requests.post(url, json= json)
print(s.text)
end =  timer()
print(timedelta(seconds=end-start))