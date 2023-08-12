const fs = require('fs')
const express = require('express')
const router = express()

const mediaController = require('../controllers/media')

router.get('/image/:imageName', mediaController.fetchImage)

module.exports = router