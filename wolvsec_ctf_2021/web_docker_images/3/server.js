let secret = require('./secret.js');
let express = require('express');
let app = express();

app.get('/', function(req, res) {
    res.sendFile(__filename);
});

app.get('/flag', function(req, res) {
    if (!req.query.value) {
        res.send('Please provide a query string parameter like: ?value=<something>');
    }
    else if (req.query.value !== 'itchy,knee' && req.query.value == 'itchy,knee') {
        res.send(secret.flag);
    }
    else {
        res.send('Sorry, please try again.');
    }
});

let port = 12343;
app.listen(port, () => {
    console.log('express listening on ' + port);
});
