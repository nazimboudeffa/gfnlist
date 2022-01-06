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

/*
app.get('/list', function (req, res) {
  res.render('list')
})
*/

app.get('/offers', function (req, res) {
  res.render('offers')
})

app.get('/social', function (req, res) {
  res.render('social')
})

app.get('/changelog', function (req, res) {
  res.render('changelog')
})

app.get('/info', function (req, res) {
  res.render('info')
})

let port = 3000;

app.listen(port, function () {
  console.log('GFNList app listening on port 3000!')
})
