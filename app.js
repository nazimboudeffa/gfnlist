const fs = require('fs')
const express = require('express')
const app = express()
const ejs = require('ejs')
const path = require('path')

// set the view engine to ejs
app.set('view engine', 'ejs')
app.set('views', path.join(__dirname, '/public'))

app.use(express.static('public'));

app.get('/', function (req, res) {
  res.render('index')
})

app.get('/changelog', function (req, res) {
  res.render('changelog')
})

let port = 3000;

app.listen(port, function () {
  console.log('Example app listening on port 3000!')
})
