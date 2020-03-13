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
pythonanywhere_user=os.environ['PYTHON_USERNAME']
pythonanywhere_target=os.environ['TARGET_PATH'] 


url = "https://www.pythonanywhere.com/api/v0/user/"+pythonanywhere_user+"/files/path/home/"+pythonanywhere_user+pythonanywhere_target
print(url)
payload = {}
file = open(file_path,'rb')


headers = {
  'Authorization': 'Token {pythonanywhere_key}'.format(pythonanywhere_key=pythonanywhere_key)
}

response = requests.request("POST", url, headers=headers, data = payload, files = {'content': file})

print(response.content)

