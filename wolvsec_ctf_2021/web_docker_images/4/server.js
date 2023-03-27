let secret = require('./secret.js');
let express = require('express');
let app = express();
const bodyParser = require('body-parser');
app.use(bodyParser.json())

app.get('/', function(req, res) {
    res.sendFile(__filename);
});

app.post('/flag', function(req, res) {
    const postedObject = req.body;
    if (typeof postedObject !== 'object' || Object.keys(postedObject).length === 0) {
        res.send('Please POST an application/json with a property');
    }
    else {
        const localObject = {}

        for (key of Object.keys(postedObject)) {
            localObject[key] = postedObject[key];
        }

        if (postedObject.secret === undefined && localObject.secret === 'flag') {
            res.send(secret.flag);
        }
        else {
            res.send('Sorry, please try again.  Your posted object: ' + JSON.stringify(postedObject));
        }
    }
});

let port = 12344;
app.listen(port, () => {
    console.log('express listening on ' + port);
});
