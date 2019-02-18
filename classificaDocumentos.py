import json
import os
import re
import pytesseract
import pdftotext
from PIL import Image
from watson_developer_cloud import NaturalLanguageClassifierV1
from wand.image import Image as Img

def processaDoc(doc):
    data = ''
    try:
        pdf = pdftotext.PDF(doc)
    except:
        return data
    # aqui precisa ver se é texto ou imagem
    # se texto, pega os primeiros 2048 caracteres 
    for page in pdf:
        data+=page
    
    data = ' '.join(data.split())
    data = data.replace('\n', ' ')
    data = data.replace('\r', '')
    data = data.replace('\t', '')
    return data

def processaPDF():
    try:
        with Img(filename='processar.pdf', resolution=300) as img:
            img.compression_quality = 99
            with open('processar.jpg', 'wb') as f:
                img.save(file=f)
        text = pytesseract.image_to_string('processar.jpg')
        os.remove('processar.jpg')
        os.remove('processar.pdf')
    except:
        text = ''
    return text
