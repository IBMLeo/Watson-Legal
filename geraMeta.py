import json
from collections import defaultdict
from var import cliente, clienteNomes

data = json.load(open('files.json'))

movimentacoesProcessadas = 473648
sentencasEncontradas = len(data[cliente])

dataCliente = data[cliente]
dataCliente['meta'] = {}

decisao = defaultdict(int)
onus = defaultdict(int)
contraFavor = defaultdict(int)
contraFavor['Ativo'] = 0
contraFavor['Passivo'] = 0
forum = defaultdict(int)
vara = defaultdict(int)
valor = defaultdict(int)
dataProcesso = defaultdict(int)

for processo in dataCliente:
    if "Decisao" in dataCliente[processo]:
        decisao[dataCliente[processo]["Decisao"]] += 1
    if "Onus" in dataCliente[processo]:
        onus[dataCliente[processo]["Onus"]] += 1
    if "Forum" in dataCliente[processo]:
        f = dataCliente[processo]["Forum"]
        f = f.replace('"',  '')
        forum[f] += 1
    if "Vara" in dataCliente[processo]:
        vara[dataCliente[processo]["Vara"]] += 1
    if "Valor" in dataCliente[processo]:
        v = dataCliente[processo]["Valor"]
        v = v.split(',')
        v = v[0]
        value = int(v)
        if value == 0:
            valor["0"] += 1
        elif value < 5000:
            valor["0-5000"] += 1
        elif value < 15000:
            valor["5000-15000"] += 1
        elif value < 50000:
            valor["15000-50000"] += 1
        elif value < 100000:
            valor["50000-100000"] += 1
        elif value > 100000:
            valor["100000+"] += 1
    if "Data" in dataCliente[processo]:
        dataProcesso[dataCliente[processo]["Data"]] += 1
    if "Autor" in dataCliente[processo]:
        autor = dataCliente[processo]["Autor"]
        if any(x.lower() in autor.split(' ') for x in clienteNomes):
            contraFavor["Ativo"] += 1
        else:
            contraFavor["Passivo"] += 1

metaInformacao = {
    "Decisao": dict(decisao),
    "Onus": dict(onus),
    "DecisaoContraFavor": dict(contraFavor),
    "Forum": dict(forum),
    "Vara": dict(vara),
    "Data": dict(dataProcesso),
    "Valor": dict(valor),
    "movimentacoesProcessadas": movimentacoesProcessadas,
    "sentencasEncontradas": sentencasEncontradas,
    "sentencasProcessadas": len(data[cliente])-1
}

if "meta" in dataCliente:
    del dataCliente["meta"]

dataCliente['meta'] = metaInformacao
data[cliente] = dataCliente

with open('files.json', 'w') as f:
    json.dump(data, f, indent=2)
