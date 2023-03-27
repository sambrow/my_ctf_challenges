const express = require('express');
const app = express();
const bodyParser = require('body-parser');
app.use(bodyParser.text({type: 'text/*', inflate: false, limit: 5000}))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }));

const fs = require('fs');
const os = require('os');
const { execSync } = require("child_process");

const parser = require('fast-xml-parser');
const he = require('he');

const XML_OPTIONS = {
    attributeNamePrefix : "@_",
    attrNodeName: "attr", //default is 'false'
    textNodeName : "#text",
    ignoreAttributes : true,
    ignoreNameSpace : false,
    allowBooleanAttributes : false,
    parseNodeValue : true,
    parseAttributeValue : false,
    trimValues: true,
    cdataTagName: "__cdata", //default is 'false'
    cdataPositionChar: "\\c",
    parseTrueNumberOnly: false,
    arrayMode: false, //"strict"
    attrValueProcessor: (val, attrName) => he.decode(val, {isAttributeValue: true}),//default is a=>a
    tagValueProcessor : (val, tagName) => he.decode(val), //default is a=>a
    stopNodes: ["parse-me-as-string"]
};


let xmlData = `<?xml version="1.0" standalone="no" ?>
<!DOCTYPE dt [<!ENTITY file SYSTEM "/Users/sambrow/hack/wolvsec_ctf_2021/docker/5/flag.txt">]>
<root>
<name>&file;</name>
<color>blue</color>
</root>
`;

class ParsedResult {
    constructor(parsedData, errorMessage) {
        this.parsedData = parsedData;
        this.errorMessage = errorMessage;
    }
}

function htmlEscape(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/'/g, "&#39;")
        .replace(/"/g, '&#34;')
        .replace(/>/g, '&gt;')
        .replace(/</g, '&lt;');
}

function parseXMLFile(filePath) {
    try {
        // couldn't find an npm xml parser that would expand file entities :(
        let parsedXML = execSync('xmllint --noent ' + filePath).toString();
        return new ParsedResult(parsedXML, null);
    }
    catch (error) {
        let message = error.message;
        let lines = message.split('\n');

        // first line likely mentions xmllint and our temporary filePath, remove this if it is there
        if (lines.length > 0 && lines[0].indexOf('xmllint') > 0) {
            lines.splice(0, 1);
        }
        let redactedMessage = lines.join('\n');
        return new ParsedResult(null, redactedMessage);
    }
}

function parseXMLString(xmlData) {
    const filePath = os.tmpdir() + '/ctf' + Math.random().toString(36) + '.xml';

    const xmlBuffer = Buffer.from(xmlData, 'utf-8');
    fs.writeFileSync(filePath, xmlBuffer);
    const parseXMLResult = parseXMLFile(filePath);
    fs.unlink(filePath, () => {/*ignore*/});

    return parseXMLResult;
}

function parseXMLStringAsJSON(xmlData) {
    const parseXMLResult = parseXMLString(xmlData);
    if (parseXMLResult.errorMessage) {
        return new ParsedResult(null, parseXMLResult.errorMessage);
    }

    try{
        const xmlObj = parser.parse(parseXMLResult.parsedData, XML_OPTIONS, true);

        let name = 'undefined';
        let color = 'undefined';

        const keys = Object.keys(xmlObj);
        if (keys.length > 0) {
            const key = keys[0]
            name = xmlObj[key].name;
            color = xmlObj[key].color;
        }

        const jsonResult = {"name": name, "color": color};
        return new ParsedResult(jsonResult, null);
    }
    catch(error) {
        return new ParsedResult(null, error.message);
    }
}

// const result = parseXMLStringAsJSON(xmlData);
// console.log(JSON.stringify(result));


app.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html');
});

app.post('/submit', function(req, res) {
    let name = 'undefined';
    let color = 'undefined';
    let errorMessage = null;

    if (typeof req.body === 'object') {
        name = req.body.name;
        color = req.body.color;
    }
    else if (typeof req.body === 'string') {
        const parsedResult = parseXMLStringAsJSON(req.body);
        if (parsedResult.errorMessage) {
            errorMessage = parsedResult.errorMessage;
        }
        else {
            name = parsedResult.parsedData.name;
            color = parsedResult.parsedData.color;
        }
    }

    if (errorMessage) {
        res.send(errorMessage);
    }
    else {
        // build up html
        name = name || 'undefined';
        color = color || 'undefined';

        let escapedName = htmlEscape(name);
        let escapedColor = htmlEscape(color);

        const POST_RESPONSE_TEMPLATE = `<html>
<body>
<p>Hi ${escapedName}!</p>
<p>My favorite color is also ${escapedColor}.</p>
</body>
</html>
`;
        res.contentType('text/html');
        res.send(POST_RESPONSE_TEMPLATE);
    }
});


let port = 12345;
app.listen(port, () => {
    console.log('express listening on ' + port);
});

