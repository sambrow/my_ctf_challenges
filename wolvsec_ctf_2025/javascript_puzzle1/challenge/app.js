const express = require('express')

const app = express()
const port = 8000

app.get('/', (req, res) => {
    try {
        const username = req.query.username || 'Guest'
        const output = 'Hello ' + username
        res.send(output)
    }
    catch (error) {
        res.sendFile(__dirname + '/flag.txt')
    }
})

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`)
})