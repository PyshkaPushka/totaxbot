import requests
import os
import json




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

output_dict = [x for x in input_dict if x['name'] == 'dev_console']



for d in output_dict: 
    for k, v in d.items(): 
        if k=='id':
           console_id=v


print(console_id)


response = requests.request("GET", "https://www.pythonanywhere.com/api/v0/user/totahbot/consoles/"+str(console_id), headers=headers, data = payload)

print(response.content)