const express = require('express')
const cookieParser = require('cookie-parser')
const jwt = require('jsonwebtoken')
const fs = require('fs')

const TOKEN_SECRET = fs.readFileSync(__dirname + '/public/TOKEN_SECRET.txt', 'utf8')

const PORT = 3000

const COOKIE_NAME = 'access-token'

const FLAG = 'wctf{jw7_l34rn1n6_15_fun_135624154}'

const app = express()
app.set("query parser", "simple")
app.use(cookieParser())
app.use(express.static(__dirname + '/public'))

function generateAccessToken(username, isAdmin) {
    return jwt.sign({ username, isAdmin }, TOKEN_SECRET, { expiresIn: '18000s' });
}

app.get('/get-token', (req, res) => {
    const username = req.query.username || 'bob'
    res.cookie(COOKIE_NAME, generateAccessToken(username, false))
    res.send(
        `
        You now have a cookie named <b>${COOKIE_NAME}</b>.<br/><br/>
        It will be sent on all future requests to this web app.<br/><br/>
        To continue, please visit <a href="/page3.html">this page</a>.
        `)
})


app.get('/get-flag', (req, res) => {
    token = req.cookies[COOKIE_NAME]

    if (!token) {
        res.send('You are missing your token. Go back to the home page and get one!')
        return
    }

    let decoded
    try {
        decoded = jwt.verify(token, TOKEN_SECRET, { algorithms: ['HS256'] })
    }
    catch (e) {
        res.send(`The token failed verification: ${e.message}`)
        return
    }

    let message = `Your JWT validated perfectly and contains: <br/><br/>${JSON.stringify(decoded)}<br/><br/>`

    if (decoded.isAdmin) {
        message += `Hello ${decoded.username}, since you are an admin, here is your flag: <b>${FLAG}</b>`
    }
    else {
        message += `Hello ${decoded.username}, since you are NOT an admin, you cannot have the flag.`
    }
    
    res.send(message)
})
  


app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`)
})