let express = require('express');
let app = express();

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html');
});

app.get('/robots.txt', function(req, res) {
    res.setHeader('Content-Type', 'text/plain');
    res.send("user-agent: kilroy\n/hidden892734569.html");
});

app.get('/hidden892734569.html', function(req, res) {
    res.sendFile(__dirname + '/hidden.html');
});

app.get('/style.css', function(req, res) {
    res.redirect('/style/style.css')
});

app.get('/style/style.css', function(req, res) {
    res.redirect('/layout/style.css')
});

app.get('/layout/style.css', function(req, res) {
    res.setHeader('Interesting', 'TXIuIFJvYm90byBzZXo6IFRyeSBnb2luZyB0byAvY3NzL3N0eWxlNzU2NDg3NS5jc3M=')
    res.redirect('/css/style.css')
});

app.get('/css/style.css', function(req, res) {
    res.sendFile(__dirname + '/style.css')
});

app.get('/css/style7564875.css', function(req, res) {
    res.setHeader('Content-Type', 'text/plain');

    let userAgent = req.headers["user-agent"] || 'undefined';
    if (userAgent) {
        userAgent = userAgent.toLowerCase();
    }
    if (userAgent.indexOf('kilroy') < 0) {
        res.send('Mr. Roboto sez: You are almost there.  Maybe a different User-Agent: would help. Your User-Agent: ' + req.headers["user-agent"]);
    }
    else {
        res.send('Mr. Roboto is proud of you! GLSC{d0m0_4r19470u_h4ck3r}')
    }
});

let port = 12342;
app.listen(port, () => {
    console.log('express listening on ' + port);
});
