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

