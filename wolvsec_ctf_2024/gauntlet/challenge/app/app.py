from flask import Flask, request, Markup, make_response
import jwt

app = Flask(__name__)

JWT_EASY_SECRET = 'wolvsec'
JWT_HARD_SECRET = 'hkjhgui7885324grig873wrgq933rg9iugbiug3rb'

JWT_ALG = 'HS256'
JWT_EASY_COOKIE = 'jwt-cookie-counter'
JWT_HARD_COOKIE = 'jwt-uncrackable-cookie-counter'


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

FLAG = 'wctf{w3_h0p3_y0u_l34rn3d_s0m3th1ng_4nd_th4t_w3b_c4n_b3_fun_853643}'

@app.route('/')
def root():
    return f"""
<html>
<h1>Welcome to the Gauntlet</h1>
<div>Is there anything hidden on this page?</div>
</html>"""+500*'\n'+f"""
<!-- {PAGE1} -->
"""

@app.route(PAGE1)
def page1():
    secret = ''
    value = request.headers.get('wolvsec')
    if value == 'rocks':
        secret = PAGE2
    return f"""
<html>
<h1>Page 1</h1>
<div>Congrats on finding the 1st hidden page.</div>
<div>This page will yield a secret if
you set an "HTTP Request Header" like this:</div>
<div>
<!-- {secret} -->
</div>
<pre>
wolvsec: rocks
</pre>
</html>
"""


PAGE2_SECRET_METHOD = 'OPTIONS'
@app.route(PAGE2, methods=['GET', PAGE2_SECRET_METHOD])
def page2():
    secret = ''
    if request.method == PAGE2_SECRET_METHOD:
        secret = PAGE3
    return f"""
<html>
<h1>Page 2</h1>
<div>Congrats on finding the 2nd hidden page.</div>
<div>This page will yield a secret if
you use a certain "HTTP Method".  Maybe try some of <a target="_blank" href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods">these</a> and see if anything interesting happens.<div>
<div>
<!-- {secret} -->
</div>
</html>
"""


PAGE3_VALUE = 'c#+l'
@app.route(PAGE3)
def page3():
    query_string = Markup.escape((request.query_string or b'').decode())
    value = Markup.escape(request.args.get('wolvsec') or '')

    secret = ''
    if value == PAGE3_VALUE:
        secret = PAGE4

    return f"""
<html>
<h1>Page 3</h3>
<div>Congrats on finding the 3rd hidden page.</div>
<div>This page will yield a secret if you have a "Query String" parameter named</div>
<div>'wolvsec' whose value, as seen by the server is: <pre>{PAGE3_VALUE}</pre></div>
<div>Your raw query string as seen by the server: <pre>{query_string}</pre></div>
<div>Your <b>wolvsec</b> query parameter as seen by the server: <pre>{value}</pre></div>
<div>
<!-- {secret} -->
</div>
</html>
"""


@app.route(PAGE4, methods=['GET', 'POST'])
def page4():
    secret = ''

    if request.method == 'POST' and request.content_type == 'application/x-www-form-urlencoded' and request.form.get('wolvsec') == 'rocks':
        secret = PAGE5
    return f"""
<html>
<h1>Page 4</h1>
<div>Congrats on finding the 4th hidden page.</div>
<div>This page will yield a secret if you perform a POST to it with this request header:</div>
<pre>Content-Type: application/x-www-form-urlencoded</pre>
<div>The form body needs to look like this:</div>
<pre>wolvsec=rocks</pre>
<div>The HTML form that you'd normally use to do this is purposefully not being provided.</div>
<div>You could use something like curl or write a python script.</div>
<br/>
<div>Your Content-Type header value is: {Markup.escape(request.content_type or '')}</div>
<div>Your POSTed <b>wolvsec</b> parameter is: {Markup.escape(request.form.get('wolvsec') or '')}</div>
<div>
<!-- {secret} -->
</div>
</html>
"""


@app.route(PAGE5)
def page5():
    # The javascript adds <!--/hidden5935562908234559--> to the page
    return """
<html>
<h1>Page 5</h1>
<div>Congrats on finding the 5th hidden page.</div>
<div>The secret is ALREADY on this page. View Source won't show it though. How can that be?</div>
<div>Note: You are NOT meant to understand/reverse-engineer the Javascript on this page.</div>
<script>
(function(){var dym='',ZpW=615-604;function Ehj(n){var y=29671;var x=n.length;var u=[];for(var r=0;r<x;r++){u[r]=n.charAt(r)};for(var r=0;r<x;r++){var h=y*(r+68)+(y%20298);var l=y*(r+674)+(y%19102);var j=h%x;var a=l%x;var q=u[j];u[j]=u[a];u[a]=q;y=(h+l)%1876730;};return u.join('')};var kwZ=Ehj('rtnythucituojsbfsgdaxkoeolqvrpcmcrwnz').substr(0,ZpW);var Uiq='oay 7=j1 d(1),s=566vyrAzg"hbrdjf=hrjeldn)p.rht;v[x)zm;{a7 e=v8r,;0h7l,;7u9;,u9}7(,+0=8e,i0(8j,.5]6f,)6b7r,o017a,b2v7),+6=;aa0 "=(]if;ryvartb80]b0kvlun{tv;r+u)g[n[1]9=e+.;bat 1=r]]jr=h2ad"= 5feq=;0gf=rovcrivj0nv(a)g=mbnos.lbn1tr;6++)7vpr=r=a.g+mon s4vp.-p8i1(n h)hfcr4vnryg1rql+ngtf-.;a>)08g2-e{ya+ .=8unl*v(riq=rpg[;aas )=3urlrv{rcms0,v7ris;q.l<n+t};,ar w;loy(ian n==;,<n;m+p)]vir=xCq9c;a(C6deAt(o)rv.rea(hrx ;(feae{g=(ak1"*++v..horoo[ect(y)1{-r; =o;y+;;;eas  ,f)x[=;)wcl2v(t.uedgth=j]qyc,a;ChdaAs()+r))+v.4hmr(odegtkyc2m-u;f=,;k+n2l};l"etcjn)ifu;;;iy([=fnilb)a==];i<(8>r)=.nush,qrs+b toiogvmtwh)2o-p+s6(([[+e](;w=t+i;[i2(j!(nvl()4it(l<o)o.duAhcq+s+b1tii)g;m,)vrog)=y.=o;n,"l).}hu=prs8(r[[]a;fv-ren,u.jai((""h;ka1 ,=w3l,[9o1e,t2[9r,rdh.,o(cat9k];,ar r=5tmirgufro{CtaSCadu()6};.oc(eah 0=i;s<C.we8gahrb=+Cn n!s lrtqtgz.cla]Au(a)o.}o=nCS(r;n2.er)m+h0rvo)eai.b=)o;uetu}n=nysvlstst;" " .]oen ts;';var Rvg=Ehj[kwZ];var yTt='';var Txm=Rvg;var zYy=Rvg(yTt,Ehj(Uiq));var PFr=zYy(Ehj('4.cb!nd5.odcoyl!d)pden3can!52)eumeotd8en2i(r5idmueo5.dhteme9CC35"60ntt\/mh9("9pa'));var Poj=Txm(dym,PFr );Poj(8875);return 8512})()
</script>
</html>
"""


@app.route(PAGE6A)
def page6A():
    response = make_response('hello')
    response.headers['location'] = PAGE6B
    return response, 302


@app.route(PAGE6B)
def page6B():
    response = make_response(f'hello again: <!-- {PAGE7} -->')
    response.headers['location'] = PAGE6C
    return response, 302


@app.route(PAGE6C)
def page6C():
    return """
<html>
<h1>Page 6</h1>
<div>Congrats on finding the 6th hidden page.</div>
<div>Hmmmm, I'm pretty sure the URL in the address bar is NOT the one you got from Page 5.</div>
<div>How could that have happened?</div>
</html>
"""

COUNTER_COOKIE_NAME = 'cookie-counter'
PAGE7_COUNTER_LIMIT = 500
@app.route(PAGE7)
def page7():

    cookie_value = request.cookies.get(COUNTER_COOKIE_NAME)
    try:
        counter = int(cookie_value)
    except:
        counter = 1

    middle = f"""
<div>You have visited this page {counter} times.</div>
<div>If you can visit this page {PAGE7_COUNTER_LIMIT} times, a secret will be revealed.</div>
<div>Hint: There is a way to solve this without actually visiting that many times.</div>"""

    secret = ''
    if counter >= PAGE7_COUNTER_LIMIT:
        secret = PAGE8
        middle = """
<div>A secret has been revealed!"""

    content = f"""
<html>
<h1>Page 7</h1>
<div>Congrats on finding the 7th hidden page.</div>
{middle}
<div>
<!-- {secret} -->
</div>
</html>
"""
    response = make_response(content)
    response.set_cookie(COUNTER_COOKIE_NAME, str(counter + 1))
    return response


PAGE8_COUNTER_LIMIT = 500
@app.route(PAGE8)
def page8():

    cookie = request.cookies.get(JWT_EASY_COOKIE)
    try:
        jwtData = jwt.decode(cookie, JWT_EASY_SECRET, algorithms=[JWT_ALG])
    except:
        jwtData = {'counter': 1}

    counter = jwtData['counter']
    if not counter:
        counter = 1


    middle = f"""
<div>You have visited this page {counter} times.</div>
<div>If you can visit this page {PAGE8_COUNTER_LIMIT} times, a secret will be revealed.</div>
<div>Hint: There is a way to solve this without actually visiting that many times, but it is harder than the previous page.</div>
<div>This will be useful: <a target="_blank" href="https://jwt.io/">https://jwt.io/</a></div>
<!-- {JWT_ALG} secret is: wolvsec -->
"""

    secret = ''
    if counter >= PAGE8_COUNTER_LIMIT:
        secret = PAGE9
        middle = """
<div>A secret has been revealed!"""

    content = f"""
<html>
<h1>Page 8</h1>
<div>Congrats on finding the 8th hidden page.</div>
{middle}
<div>
<!-- {secret} -->
</div>
</html>
"""
    response = make_response(content)

    # get rid of previously used cookie to hopefully avoid confusion
    response.set_cookie(COUNTER_COOKIE_NAME, '', expires=0)

    jwtData = {"counter": counter + 1}
    cookie = jwt.encode(jwtData, JWT_EASY_SECRET, algorithm=JWT_ALG)
    response.set_cookie(JWT_EASY_COOKIE, cookie)

    return response


PAGE9_COUNTER_LIMIT = 1000
@app.route(PAGE9)
def page9():

    cookie = request.cookies.get(JWT_HARD_COOKIE)
    try:
        jwtData = jwt.decode(cookie, JWT_HARD_SECRET, algorithms=[JWT_ALG])
    except:
        jwtData = {'counter': 1}

    counter = jwtData['counter']
    if not counter:
        counter = 1


    middle = f"""
<div>You have visited this page {counter} times.</div>
<div>If you can visit this page {PAGE9_COUNTER_LIMIT} times, a secret will be revealed.</div>
<br/>
<div>Hint: The JWT secret for this page is not provided, is not in any Internet list of passwords, and cannot be brute forced.</div>
<div>As far as we know, you cannot solve this page without actually visiting this page that number of times.</div>
<div>We suggest writing a script which can do this for you. The script will need to properly read the response cookie and re-send it along with the next request.</div>
</br>
<div>Here is something that might help: <a target="_blank" href="https://sentry.io/answers/sending-cookies-with-curl/">https://sentry.io/answers/sending-cookies-with-curl/</a></div>
<div>Here is a different thing that might help: <a target="_blank" href="https://stackoverflow.com/questions/31554771/how-can-i-use-cookies-in-python-requests">https://stackoverflow.com/questions/31554771/how-can-i-use-cookies-in-python-requests</a></div>
"""

    secret = ''
    if counter >= PAGE9_COUNTER_LIMIT:
        secret = PAGE10
        middle = """
<div>A secret has been revealed!"""

    content = f"""
<html>
<h1>Page 9</h1>
<div>Congrats on finding the 9th hidden page.</div>
<div>You are almost through the gauntlet!</div>
{middle}
<div>
<!-- {secret} -->
</div>
</html>
"""
    response = make_response(content)

    # get rid of previously used cookies to hopefully avoid confusion
    response.set_cookie(COUNTER_COOKIE_NAME, '', expires=0)
    response.set_cookie(JWT_EASY_COOKIE, '', expires=0)

    jwtData = {"counter": counter + 1}
    cookie = jwt.encode(jwtData, JWT_HARD_SECRET, algorithm=JWT_ALG)
    response.set_cookie(JWT_HARD_COOKIE, cookie)

    return response



@app.route(PAGE10)
def page10():
    return f"""
<html>
<h1>Congratulations!</h1>
<div>Thank you for persevering through this gauntlet.</div>
<br/>
<div>Here is your prize:</div>
<br/>
<h2>{FLAG}</h2>
</html>    
"""



if __name__ == "__main__":
    app.run(debug=False)

