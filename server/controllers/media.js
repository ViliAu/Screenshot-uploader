const fs = require('fs')

const fetchImage = (req, res, next) => {
    const imageName = req.params.imageName
    const readStream = fs.createReadStream(`media/${imageName}`)
    readStream.pipe(res)
}

module.exports = {
    fetchImage: fetchImage
}