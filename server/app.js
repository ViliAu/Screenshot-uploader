var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var uploadRouter = require('./routers/upload');
var mediaRouter = require('./routers/media');

var app = express();

const port = process.env.port ?? 3000

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.use(express.static(path.join(__dirname, 'public')));

app.use('/api/upload', uploadRouter);
app.use('/api/media', mediaRouter);

app.listen(port, () => console.log(`App listening to ${port}`))
