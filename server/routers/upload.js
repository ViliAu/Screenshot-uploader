const express = require('express')
const router = express()
const multer = require('multer')
const upload = multer({ dest: 'media/' })

const uploadController = require('../controllers/upload')

// Handles traffic to /api/upload/image route
router.post('/image', upload.single('media'), uploadController.uploadImage);

router.post('/video', upload.single('media'), uploadController.uploadImage);

module.exports = router