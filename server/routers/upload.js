const express = require('express')
const router = express()
const multer = require('multer')
const upload = multer({ dest: 'media/' })

const uploadController = require('../controllers/upload')

// Handles traffic to /image route
// TODO create a middleware for time parsing
router.post('/image', upload.single('image'), uploadController.uploadImage)

module.exports = router