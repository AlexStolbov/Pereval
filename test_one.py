import requests
import json
import random

payload = {"beauty_title": "пер. ",
           "title": "Пхия",
           "other_titles": "Триев",
           "connect": "",
           "add_time": "2021-09-22 13:18:13",
           "user": {"email": "qwerty@mail.ru",
                    "fam": "Пупкин",
                    "name": "Василий",
                    "otc": "Иванович",
                    "phone": "+7 555 55 55"},
           "coords": {
               "latitude": "45.3842",
               "longitude": "7.1525",
               "height": "1200"},
           "level": {"winter": "",
                     "summer": "1А",
                     "autumn": "1А",
                     "spring": ""},
           "images": [{"data": "<image1>", "title": "Седловина"},
                      {"data": "<image2>", "title": "Подъём"}]
           }

transfer = json.dumps(payload)
# print(transfer)
# r = requests.post('http://localhost:8000/submitData/', data=transfer)

# POST
# r = requests.post('http://localhost:8000/submitData/', json=payload)

# GET
r = requests.get('http://localhost:8000/submitData/39')
# GET list
email1 = 'ss@mm.com'
email2 = 'qwerty@mail.ru'
# r = requests.get(f'http://localhost:8000/submitData/?user__email={email2}')

# Patch
payload['coords']['latitude'] = str(random.randrange(1000))
# payload['user']['name'] = 'any name'
# print(payload)
# r = requests.patch('http://localhost:8000/submitData/36/', json=payload)

print(f'headers: {r.headers}')
# pprint.pprint(f'text: {json.loads(r.text)}')
# print(f'text1: {json.dumps(json.loads(r.text), sort_keys=True, indent=4)}')
# print(f'text1: {json.dumps(r.text, sort_keys=True, indent=4)}')
print(f'text1: {r.text}')
f = open('/mnt/S970/Tmp/pereval_debug.html', 'w')
f.write(r.text)
