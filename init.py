# -*- coding: utf-8 -*-

import json
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from collections import OrderedDict
from datetime import datetime
import boto3
from boto3.s3.transfer import TransferConfig

app = Flask(__name__)

FLASK_DEBUG = 1
ARQUIVOS = 'Clientes'
app.config['ARQUIVOS'] = ARQUIVOS
app.config['FLASK_DEBUG'] = FLASK_DEBUG


@app.route('/cria', methods=['POST'])
def cria():
    cliente = request.form["text"]
    if not os.path.exists('Clientes/%s' % (cliente)):
        os.makedirs('Clientes/%s' % (cliente))
        os.makedirs('Clientes/%s/1movimentacao' % (cliente))
        os.makedirs('Clientes/%s/2processo' % (cliente))
        os.makedirs('Clientes/%s/3inicial' % (cliente))
        os.makedirs('Clientes/%s/4sentenca' % (cliente))
    with open('files.json') as file:
        data = json.load(file)
    data[request.form["text"]] = {}
    with open('files.json', 'w') as file:
        json.dump(data, file)
    return 'workspace criado'


@app.route('/criaCliente')
def criaCliente():
    with open('files.json') as file:
        try:
            listaCliente = json.load(file)
        except:
            return render_template('criaCliente.html')
    return render_template('criaCliente.html', clientes=listaCliente)


@app.route('/cliente/<cliente>')
def profile(cliente):
    with open('files.json') as file:
        data = json.load(file)
        try:
            listaCliente = data[cliente]
        except:
            return render_template('cliente.html', cliente='não encontrado')
    return render_template('cliente.html', cliente=cliente, json=listaCliente)


@app.route('/arquivos/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['ARQUIVOS'], filename)


@app.route('/processa')
def processa():
    return render_template('processa.html')

@app.route('/documento', methods=['GET'])
def documento():
    tipo = request.args.get('tipo').lower()
    cnj = request.args.get('cnj').replace('.', '').replace('-', '').lower()

    if request.args.get('cliente').lower() == 'oi':
        b = 'elaw-poc-oi'
    elif request.args.get('cliente').lower() == 'santander':
        b = 'elaw-poc-001'
    elif request.args.get('cliente').lower() == 'claro':
        b = 'elaw-poc-claro'
    elif request.args.get('cliente').lower() == 'recovery':
        b = 'elaw-poc-recovery'

    endpoint = 'https://s3-api.us-geo.objectstorage.softlayer.net'
    session = boto3.Session(
        aws_access_key_id= 'E0iOL48efro7w7lDU8Qz',
        aws_secret_access_key= 'cGfutAKpUHxKfZK2xTmnRVR8ZK009zGef7wOS1KQ'
    )
    
    config = TransferConfig(use_threads=False)
    s3 = session.resource('s3', endpoint_url=endpoint)
    bucket = s3.Bucket(b)
    objs = bucket.objects.filter(Prefix=cnj)

    if tipo == 'inicial':
        objsInicial = [obj for obj in objs if "inicial" in obj.key.lower()]
        if len(objsInicial) == 0:
            objs = [obj for obj in objs if "peticao" in obj.key.lower()]
        else:
            objs = objsInicial
        s3.Bucket(bucket.name).download_file(objs[0].key, 'static/inicial.pdf', Config=config)
        return render_template('Documento.html', tipo=tipo, time=datetime.utcnow())
    else:
        objs = [obj for obj in objs if "sentenca" in obj.key.lower()]
        s3.Bucket(bucket.name).download_file(objs[-1].key, 'static/sentenca.pdf', Config=config)
        return render_template('Documento.html', tipo=tipo, time=datetime.utcnow())

@app.route('/dashboard/<cliente>')
def dashboard(cliente):
    with open('files.json') as file:
        data = json.load(file)
    try:
        data = data[cliente]["meta"]
    except:
        return render_template('Dashboard.html', cliente='não encontrado', reversed=True)

    forum = data['Forum']
    forum = sorted(forum.items(), reverse=True, key=lambda x: x[1])
    forum = forum[:10]

    Data = data['Data']
    dataOrdenado = sorted(Data.items(), key=lambda x:datetime.strptime(x[0], '%d/%m/%Y'), reverse=False)
    dataOrdenado = dataOrdenado[-90:]

    Onus = data['Onus']
    Onus['Não encontrado'] = abs(int(Onus['Não encontrado']) - int(data['Decisao']['Decisão Extinta sem resolução']))
    Onus['Decisão Extinta sem resolução'] = data['Decisao']['Decisão Extinta sem resolução']
    if 'SentencasPorTipo' in data:
        SentencasPorTipo = data['SentencasPorTipo']
    else:
        SentencasPorTipo = []
    print(cliente+'\n\n\n')
    print(json.dumps(data['DecisaoContraFavor'])+'\n\n\n')
    print(json.dumps(Onus)+'\n\n\n')
    

    return render_template('Dashboard.html',
                           cliente=cliente,
                           json=data,
                           decisao_labels=list(data['Decisao'].keys()),
                           decisao_values=list(data['Decisao'].values()),
                           onus=Onus,
                           onus_labels=list(Onus.keys()),
                           onus_values=list(Onus.values()),
                           caf=data['DecisaoContraFavor'],
                           caf_labels=list(data['DecisaoContraFavor'].keys()),
                           caf_values=list(data['DecisaoContraFavor'].values()),
                           forum_labels=[f[0] for f in forum],
                           forum_values=[f[1] for f in forum],
                           valor=data['Valor'],
                           valor_labels = list(data['Valor'].keys()),
                           valor_values = list(data['Valor'].values()),
                           Data_labels=[D[0] for D in dataOrdenado],
                           Data_values=[D[1] for D in dataOrdenado],
                           SentencasPorTipo = SentencasPorTipo,
                           SentencasPorTipoLabels = list(SentencasPorTipo)
                           )


app.run()
