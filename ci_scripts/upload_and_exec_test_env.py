import requests
import os
import time

import json

def find_console_id(content):
   console_id=""
   if isinstance(content, list): 
      for d in content: 
          for k, v in d.items(): 
             if k=='id':
                 console_id=v
   elif isinstance(content, dict): 
      console_id=content.get("id")

   return console_id


pythonanywhere_key= os.environ['PYTHON_API_KEY']
file_path=os.environ['FILE_PATH'] 

url = "https://www.pythonanywhere.com/api/v0/user/totahbot/files/path/home/totahbot/dev/devbot.py"

payload = {}
file = open(file_path,'rb')


headers = {
  'Authorization': 'Token {pythonanywhere_key}'.format(pythonanywhere_key=pythonanywhere_key)
}

response = requests.request("POST", url, headers=headers, data = payload, files = {'content': file})

print(response.content)

