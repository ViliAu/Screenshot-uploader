
const uploadImage = (req, res, next) => {
    console.log("Hello");
    res.status(200).send("Not implemented")
}

const uploadVideo = (req, res, next) => {
    res.status(501).send("Not implemented")
    
}

module.exports = {
    uploadImage: uploadImage
}