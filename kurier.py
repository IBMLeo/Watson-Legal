import requests
import json
from datetime import datetime
from var import cliente, kurieruser, kurierpassword

url = "http://www.kurierservicos.com.br/wsservicos/api/KAndamento/ConsultarDadosProcessos"

processos = json.load(open('files.json'))

processosCliente = processos[cliente]

for key in processosCliente:
    if key == 'meta':
        break
    payload = "[\""+key+"\"]"
    
    headers = {
        'Cache-Control': "no-cache",
        'Content-Type': "application/json",
        'cache-control': "no-cache",
    }
    try:
        response = requests.request("POST", url, data=payload, headers=headers, auth=(kurieruser, kurierpassword))
    except Exception as e:
        print(e)

    resultado = response.json()

    print(resultado)

    if len(resultado) > 0:
        processosCliente[key]['Forum'] = resultado[0]['Forum']
        processosCliente[key]['TipoProcesso'] = resultado[0]['TipoProcesso']
        processosCliente[key]['Vara'] = resultado[0]['Vara']
        processosCliente[key]['Reu'] = resultado[0]['Reu']
        processosCliente[key]['Autor'] = resultado[0]['Autor']
        processosCliente[key]['Valor'] = resultado[0]['Valor']
        processosCliente[key]['AdvogadoReu'] = resultado[0]['AdvogadoReu']
        processosCliente[key]['AdvogadoAutor'] = resultado[0]['AdvogadoAutor']
        processosCliente[key]['DataAtualizacaoProcesso'] = str(datetime.strptime(resultado[0]['DataAtualizacaoProcesso'], '%Y-%m-%dT%I:%M:%S').strftime('%d/%M/%Y'))
    print(key)

processos[cliente] = processosCliente

with open('files.json', 'w') as file:
    json.dump(processos, file)