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



response = requests.request("GET", "https://www.pythonanywhere.com/api/v0/user/totahbot/consoles/", headers=headers, data = payload)


input_dict = json.loads(response.content)

output_dict = [x for x in input_dict if x['working_directory'] == '/home/totahbot/dev/']
print(output_dict)


console_id=find_console_id(output_dict)

print(console_id)

if console_id != "":
   response = requests.request("DELETE", "https://www.pythonanywhere.com/api/v0/user/totahbot/consoles/"+str(console_id), headers=headers, data = payload)




headers = {
  'Content-Type': 'application/json',
    'Authorization': 'Token {pythonanywhere_key}'.format(pythonanywhere_key=pythonanywhere_key)
}
url = "https://www.pythonanywhere.com/api/v0/user/totahbot/consoles/"

payload = "{\n\t\n\t\"executable\" : \"/bin/bash\",\n\t\"working_directory\" : \"/home/totahbot/dev/\"\n}"

response = requests.request("POST", url, headers=headers, data = payload)
print(response.content)
time.sleep(5)

console_id=find_console_id(json.loads(response.content))
print(console_id)


url="https://www.pythonanywhere.com/api/v0/user/totahbot/consoles/"+str(console_id)+"/send_input/"
payload = "{\"input\" : \"pip3 install python-telegram-bot --user  \\n\"}"


response = requests.request("POST", url, headers=headers, data = payload)

print(response.content)
