const fs = require('fs')
const express = require('express')
const app = express()
const ejs = require('ejs')
const path = require('path')
// const kinguin = require('kinguin-api-es5')
require('dotenv').config();
const axios = require('axios');
const https = require('https');

const agent = new https.Agent({
  rejectUnauthorized: false
});

// set the view engine to ejs
app.set('view engine', 'ejs')
app.set('views', path.join(__dirname, '/public'))

app.use(express.static('public'));

app.get('/', function (req, res) {
  res.render('index')
})

app.get('/list', function (req, res) {
  res.render('list')
})

app.get('/offers', function (req, res) {
  res.render('offers')
})

app.get('/ig', function (req, res) {
  res.render('ig')
})

app.get('/kinguin', function (req, res) {
  res.render('kinguin')
})

app.get('/test', function (req, res) {
  res.render('test')
})

app.get('/kinguindebug/:title', async function (req, res) {
  const response = await axios.get ('https://gateway.kinguin.net/esa/api/v1'+'/products?name=' + decodeURI(req.params.title),
    {
      httpsAgent: agent,
      headers: {
        'Accept': 'application/json',
        'api-ecommerce-auth': process.env.KINGUIN_API_KEY
      }
    })
    res.json(response.data);
})

app.get('/kinguin/:title', async function (req, res) {
  const response = await axios.get ('https://gateway.kinguin.net/esa/api/v1'+'/products?name=' + decodeURI(req.params.title),
    {
      httpsAgent: agent,
      headers: {
        'Accept': 'application/json',
        'api-ecommerce-auth': process.env.KINGUIN_API_KEY
      }
    })
    res.render('kinguin-offers', { title : decodeURI(req.params.title), offers : response.data["results"] })
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
