const mongoose = require('mongoose');
const fs = require('fs');

var options = {
        ssl: true,
        sslValidate: true,
        dbName: 'POC',
        useNewUrlParser: true
};

mongoURL = "mongodb://admin:ZDOIEMYIPAOVTBTX@portal-ssl1716-16.bmix-dal-yp-c69ce889-7876-4a03-8a82-19149f2900b0.2156681883.composedb.com:62336,portal-ssl2010-0.bmix-dal-yp-c69ce889-7876-4a03-8a82-19149f2900b0.2156681883.composedb.com:62336/POC?authSource=admin&ssl=true"
mongoCollection = "recovery_andamentos_obtidos"


mongoose.connect(mongoURL, options, () => { });
var db = mongoose.connection;

db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function () {
        mongoose.connection.db.collection(mongoCollection, function (err, collection) {
                collection.count({ isProcessado: true }, (err, c) => { console.log(c) })
        });
});
