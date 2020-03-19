import sys, os, requests

BASE_URL = "https://www.pythonanywhere.com/api/v0"

if len(sys.argv) > 2:
    src_file_path = sys.argv[1]
    dst_file_path = sys.argv[2]
else:
    print('Arguments: <SourceFilePath> <DestinationFilePath>')
    sys.exit()

api_key = os.environ['PYTHON_API_KEY']
username = os.environ['PYTHON_USERNAME']

url = "{base}/user/{user}/files/path/home/{user}/{dst}".format(base=BASE_URL, user=username, dst=dst_file_path)
print("URL: ", url)
payload = {}
file = open(src_file_path, 'rb')

headers = {
    'Authorization': 'Token {0}'.format(api_key)
}

response = requests.request("POST", url, headers=headers, data=payload, files={'content': file})

print("Response: ", response.content)
