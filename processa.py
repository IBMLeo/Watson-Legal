# -*- coding: utf-8 -*-

import json
import os
from watson_developer_cloud import NaturalLanguageClassifierV1
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, RelationsOptions, KeywordsOptions, EntitiesOptions
import boto3
import pdftotext
import classificaDocumentos
from boto3.s3.transfer import TransferConfig
from var import balde, jsonFile
processos = {}
meta = {}

movimentacoesProcessadas = 0
sentencasEncontradas = 0

processos = json.load(open(jsonFile))

def conectaOS():
    global processos
    endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'
    session = boto3.Session(
        aws_access_key_id= 'E0iOL48efro7w7lDU8Qz',
        aws_secret_access_key= 'cGfutAKpUHxKfZK2xTmnRVR8ZK009zGef7wOS1KQ'
    )
    config = TransferConfig(use_threads=False)
    count = 0
    s3 = session.resource('s3', endpoint_url=endpoint)

    bucket = s3.Bucket(balde)

    processosList = list(processos)
    indiceInicial = 0

    for key in processosList[indiceInicial:]:
        fil = key.replace('.', '').replace('-', '')
        objs = bucket.objects.filter(Prefix=fil)
        if len(list(objs)) > 0:
            for obj in objs:
                if "sentenca" in obj.key.lower():
                    print('sentenca', obj.key)
                    objeto = s3.Object(bucket.name, obj.key).get()['Body']
                    output = classificaDocumentos.processaDoc(objeto)
                    if len(output) > 10:
                        classificaSentenca(output, key)
                    else:
                        s3.Bucket(bucket.name).download_file(obj.key, 'processar.pdf', Config=config)
                        output = classificaDocumentos.processaPDF()
                        classificaSentenca(output, key)
                elif "inicial" in obj.key.lower():
                    print('inicial', obj.key)
                    objeto = s3.Object(bucket.name, obj.key).get()['Body']
                    output = classificaDocumentos.processaDoc(objeto)
                    if len(output) > 10:
                        classificaInicial(output, key)
                    else:
                        s3.Bucket(bucket.name).download_file(obj.key, 'processar.pdf', Config=config)
                        output = classificaDocumentos.processaPDF()
                        classificaInicial(output, key)
        else:
            processos[key] = 'INDISPONIVEL'
        count += 1
        print('Documentos Processados: ', count+indiceInicial)
        if count % 50 == 0:
            updateDB()

def updateDB():
    global processos
    with open(jsonFile, 'w') as file:
        json.dump(processos, file)

def classificaInicial(data, cnj):
    global processos
    model = '0f8f545a-80d3-40eb-b8d5-c0cf65aabbb8'
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        iam_apikey='8DoJtndHaLOSkpBnnKucch9vG087BW8aCfqzD-Ov40F3',
        version='2018-09-21'
    )
    # model = '53a48de8-d926-45c5-b7c5-ae9e0634af99'
    # natural_language_understanding = NaturalLanguageUnderstandingV1(
    #     username='94852c79-35b1-4275-83f4-f06356dd3d1f',
    #     password='nGsfslOnDSK6',
    #     version='2018-09-21')
    try:
        response = natural_language_understanding.analyze(
            text=data,
            features=Features(entities=EntitiesOptions(model=model), relations=RelationsOptions(model=model))).get_result()
        cnpj = []
        for obj in response["entities"]:
            if obj["type"] == "CNPJ":
                cnpj.append(obj["text"])
            if obj["type"] == "CPF":
                cnpj.append(obj["text"])
        print(response)
        processos[cnj]["CPFCNPJ"] = list(set(cnpj))
        processos[cnj]["Tipo"] = "Sentenca"
    except:
        processos[cnj]["CPFCNPJ"] = []
        processos[cnj]["Tipo"] = "Sentenca"
        return

def classificaSentenca(data, cnj):
    global processos
    model = '19b70646-4870-49c6-91f7-9c9f42a97ae3'
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        iam_apikey='U1A18Ed4gVHHPe2dx__5p7xNEV3ITIdYkIHpkAj_Xqf_',
        version='2018-09-21')
    # model = '0b42c782-8863-4d29-800f-7dbce2784702'
    # natural_language_understanding = NaturalLanguageUnderstandingV1(
    #     username='82515c79-39ea-4a91-b941-ebcd5ebc2de6',
    #     password='8gPslnDmkDVD',
    #     version='2018-03-16')
    try:
        response = natural_language_understanding.analyze(
            text=data,
            features=Features(entities=EntitiesOptions(model=model), relations=RelationsOptions(model=model))).get_result()
    except:
        response = {}
    print(response)
    array = json.dumps(response)
    a = json.loads(array)
    if "entities" in a:
        for item in a["entities"]:
            if "Decisao" not in processos[cnj]:
                if item["type"] == "DecisaoProcedente":
                    processos[cnj]["Decisao"] = "Decisão Procedente"
                elif item["type"] == "DecisaoImprocedente":
                    processos[cnj]["Decisao"] = "Decisão Improcedente"
                elif item["type"] == "DecisaoParcialmenteProcedente":
                    processos[cnj]["Decisao"] = "Decisão Parcialmente Procedente"
                elif item["type"] == "DecisaoParcialmenteImprocedente":
                    processos[cnj]["Decisao"] = "Decisão Parcialmente Improcedente"
                elif item["type"] == "DecisaoExtintaComResolucao":
                    processos[cnj]["Decisao"] = "Decisão Extinta com resolução"
                elif item["type"] == "DecisaoExtintaSemResolucao":
                    processos[cnj]["Decisao"] = "Decisão Extinta sem resolução"
                else:
                    processos[cnj]["Decisao"] = "Em Análise"
            elif processos[cnj]["Decisao"] == "Em Análise":
                if item["type"] == "DecisaoProcedente":
                    processos[cnj]["Decisao"] = "Decisão Procedente"
                elif item["type"] == "DecisaoImprocedente":
                    processos[cnj]["Decisao"] = "Decisão Improcedente"
                elif item["type"] == "DecisaoParcialmenteProcedente":
                    processos[cnj]["Decisao"] = "Decisão Parcialmente Procedente"
                elif item["type"] == "DecisaoParcialmenteImprocedente":
                    processos[cnj]["Decisao"] = "Decisão Parcialmente Improcedente"
                elif item["type"] == "DecisaoExtintaComResolucao":
                    processos[cnj]["Decisao"] = "Decisão Extinta com resolução"
                elif item["type"] == "DecisaoExtintaSemResolucao":
                    processos[cnj]["Decisao"] = "Decisão Extinta sem resolução"
                else:
                    processos[cnj]["Decisao"] = "Em Análise"

            if "Onus" not in processos[cnj]:
                if item["type"] == "Sem_Onus_Da_Acao":
                    processos[cnj]["Onus"] = "Sem Ônus"
                elif item["type"] == "Com_Onus_Da_Acao":
                    processos[cnj]["Onus"] = "Com Ônus"
                else:
                    processos[cnj]["Onus"] = "Não encontrado"
            elif processos[cnj]["Onus"] == "Não encontrado":
                if item["type"] == "Sem_Onus_Da_Acao":
                    processos[cnj]["Onus"] = "Sem Ônus"
                elif item["type"] == "Com_Onus_Da_Acao":
                    processos[cnj]["Onus"] = "Com Ônus"
                else:
                    processos[cnj]["Onus"] = "Não encontrado"
    return


conectaOS()
updateDB()
