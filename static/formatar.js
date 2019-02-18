var atual = 40274.4700;

//com R$
var f = atual.toLocaleString('pt-br',{style: 'currency', currency: 'BRL'});

//sem R$
var f2 = atual.toLocaleString('pt-br', {minimumFractionDigits: 2});

console.log(f);
console.log(f2);



/*

variavel = json.load(arquivo)

for item in variavel[cliente]:
    item[valor] = item[valor].toLocaleString('pt-br',{style: 'currency', currency: 'BRL'});

json.dump(variavel, arquivo.json)
*/