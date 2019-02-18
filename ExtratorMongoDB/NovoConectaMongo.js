const mongoose = require('mongoose');
const fs = require('fs');
var http = require("http");
var request = require("request");

var options = {
    ssl: true,
    sslValidate: true,
    dbName: 'POC',
    useNewUrlParser: true
};

//VARIAVEIS PARA SE EDITAR
mongoURL = "mongodb://admin:ZDOIEMYIPAOVTBTX@portal-ssl1716-16.bmix-dal-yp-c69ce889-7876-4a03-8a82-19149f2900b0.2156681883.composedb.com:62336,portal-ssl2010-0.bmix-dal-yp-c69ce889-7876-4a03-8a82-19149f2900b0.2156681883.composedb.com:62336/POC?authSource=admin&ssl=true"
mongoCollection = "recovery_andamentos_obtidos"
arquivoOutput = "recovery.json"

mongoose.connect(mongoURL, options, () => { });

var count = 0;

function escreveMovimentacoes(cnj, descricao, data) {
    let dataJs = JSON.parse(fs.readFileSync(arquivoOutput))
    dataJs[cnj] = {}
    dataJs[cnj].descricao = descricao
    dataJs[cnj].data = data
    count += 1
    // return dataJs;
    fs.writeFileSync(arquivoOutput, JSON.stringify(dataJs, null, 4), 'utf-8')
}


function verificaDescricao(desc, cnj, dataAndamento) {
    var options = {
        method: 'POST',
        url: 'http://localhost:3001/processa',
        formData: { valor: desc }
    };

    request(options, function (error, response, body) {
        if (error) throw new Error(error);
        if (body == 'sentenca') {
            escreveMovimentacoes(cnj, desc, dataAndamento)
        }
        if (count % 50 == 0){

        }
    });
}

var db = mongoose.connection;

db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function () {
    mongoose.connection.db.collection(mongoCollection, function (err, collection) {
        collection.find({ isProcessado: false }).limit(120000).toArray((err, data) => {
            data.forEach((doc, index, col) => {
                setTimeout(() => {
                    verificaDescricao(doc.Descricao, doc.NumeracaoProcessualUnica, doc.DataAndamento)
                    collection.updateOne({ _id: doc._id }, { $set: { isProcessado: true } }, (err, tank) => {
                        if (err) console.log(err)
                    });
                    if (index % 1000 == 0) console.log(index);  
                }, index * 20)
            }) 
        });
    });
});

