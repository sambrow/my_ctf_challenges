let secret = require('./secret.js');
let express = require('express');
let app = express();

app.get('/', function(req, res) {
    res.sendFile(__filename);
});

let isThisReallyKevin = (name) => {
    if (typeof name === 'string') {
        let upperName = name.toUpperCase();
        if (upperName !== 'KEVIN') {
            let lowerName = upperName.toLowerCase();
            if (lowerName === 'kevin') {
                return true;
            }
        }
    }
    return false;
}

app.get('/flag', function(req, res) {
    if (!req.query.name) {
        res.send('Please provide a query string parameter like: ?name=<something>');
    }
    else if (isThisReallyKevin(req.query.name)) {
        res.send(secret.flag);
    }
    else {
        res.send('Kevin spells his name in an unusual way to honor his ancestor William Thomson.');
    }
});

let port = 12341;
app.listen(port, () => {
    console.log('express listening on ' + port);
});
