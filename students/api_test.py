import requests
import json

# response = requests.post(url='http://192.168.10.1:8000/students/dummy-api/',
#                          data={'matric_number': 'NAUB/18U/FCOM/SWE/017'})

response = requests.get(url='http://127.0.0.1:8000/students/dummy-api')

print(response.text)
