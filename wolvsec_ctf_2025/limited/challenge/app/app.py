# imports
from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mysqldb import MySQL

import os
import re
import socket
import ipaddress

FLAG1 = 'wctf{bu7_my5ql_h45_n0_curr3n7_qu3ry_func710n_l1k3_p0576r35_d035_25785458}'

PORT = 8000


# initialize flask
app = Flask(__name__)


def get_client_ip():
    client_ip = get_remote_address()
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        ips = [ip.strip() for ip in forwarded_for.split(',')]
        for ip in reversed(ips):
            try:
                if not ipaddress.ip_address(ip).is_private:
                    client_ip = ip
                    break
            except ValueError:
                print("invalid ip:", ip)
                pass
    print('client_ip:', client_ip)
    return client_ip


# No matter what I do, someone always tries dirbuster even when
# the source is provided.
#
# This is NOT intended to make this harder/slower to solve.
limiter = Limiter(
    app=app,
    key_func=get_client_ip,
    default_limits=["5 per second"],
    storage_uri="memory://",
)


def get_db_hostname():
    # use this when running locally with docker compose
    db_hostname = 'db'
    try:
        socket.getaddrinfo(db_hostname, 3306)
        return db_hostname
    except:
        # use this for google cloud
        return '127.0.0.1'


app.config['MYSQL_HOST'] = get_db_hostname()
app.config['MYSQL_USER'] = os.environ["MYSQL_USER"]
app.config['MYSQL_PASSWORD'] = os.environ["MYSQL_PASSWORD"]
app.config['MYSQL_DB'] = os.environ["MYSQL_DB"]

print('app.config:', app.config)

mysql = MySQL(app)


@app.route('/')
def root():
    return render_template("index.html")


@app.route('/query')
def query():
    agent = request.headers.get('User-Agent')
    if agent and 'sqlmap' in agent:
        return 'price_op too long!', 400
    
    try:
        price = float(request.args.get('price') or '0.00')
    except:
        price = 0.0

    price_op = str(request.args.get('price_op') or '>')
    if not re.match(r' ?(=|<|<=|<>|>=|>) ?', price_op):
        return 'price_op must be one of =, <, <=, <>, >=, or > (with an optional space on either side)', 400

    # allow for at most one space on either side
    if len(price_op) > 4:
        return 'price_op too long', 400

    # I'm pretty sure the LIMIT clause cannot be used for an injection
    # with MySQL 9.x
    #
    # This attack works in v5.5 but not later versions
    # https://lightless.me/archives/111.html
    limit = str(request.args.get('limit') or '1')

    query = f"""SELECT /*{FLAG1}*/category, name, price, description FROM Menu WHERE price {price_op} {price} ORDER BY 1 LIMIT {limit}"""
    print('query:', query)

    if ';' in query:
        return 'Sorry, multiple statements are not allowed', 400

    try:
        cur = mysql.connection.cursor()
        cur.execute(query)
        records = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
    except Exception as e:
        return str(e), 400

    result = [dict(zip(column_names, row)) for row in records]
    return jsonify(result)


#useful during chal development
# @app.route('/testquery')
# def test_query():
#     query = str(request.args.get('query'))
#
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute(query)
#     except Exception as e:
#         return str(e), 400
#
#     records = cur.fetchall()
#
#     column_names = [desc[0] for desc in cur.description]
#     cur.close()
#
#     result = [dict(zip(column_names, row)) for row in records]
#     return jsonify(result)


# cause grief for dirbuster
@app.route("/<path:path>")
def missing_handler(path):
    return 'page not found!', 404


# run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, threaded=True, debug=False)