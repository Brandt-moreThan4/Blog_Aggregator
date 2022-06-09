import requests
import json

import scrapefunctions as sf
POST_LIST_URL = 'http://127.0.0.1:8000/api/blogposts/'
POST_LIST_URL = 'http://127.0.0.1:8000/api/blog-external/most_recent_post'
response = requests.get(POST_LIST_URL)
content = response.text
content_list = json.loads(content)

for dicky in content_list['results']:
    for key, value in dicky.items():
        print(f'Key={key}; Value={value}')

print('lol')

