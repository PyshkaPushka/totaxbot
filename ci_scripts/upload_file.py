import requests
import os

pythonanywhere_key = os.environ['PYTHON_API_KEY']
file_path = os.environ['FILE_PATH']
pythonanywhere_user = os.environ['PYTHON_USERNAME']
pythonanywhere_target = os.environ['TARGET_PATH']

url = "https://www.pythonanywhere.com/api/v0/user/" + pythonanywhere_user + "/files/path/home/" + pythonanywhere_user + pythonanywhere_target
print(url)
payload = {}
file = open(file_path, 'rb')

headers = {
    'Authorization': 'Token {0}'.format(pythonanywhere_key)
}

response = requests.request("POST", url, headers=headers, data=payload, files={'content': file})

print(response.content)
