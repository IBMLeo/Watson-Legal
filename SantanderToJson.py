import json
from csv import DictWriter
import pandas as pd


def Export(jsonToExport):
    with open(jsonToExport, "r") as f:
        fileJson = json.load(f)

    for item in fileJson['Santander']:
        fileJson['Santander'][item]['CNJ'] = item

    finalJson = []

    for item in fileJson['Santander']:
        finalJson.append(fileJson['Santander'][item])

    with open('Santander.txt', 'w', encoding='UTF-8') as outfile:
        writer = DictWriter(outfile, delimiter=',', lineterminator='\n', fieldnames=[
                            'CNJ', 'Descricao', 'Data', "CPFCNPJ", "Tipo", 'Decisao', 'Onus', 'Forum', 'TipoProcesso', 'Vara', 'Reu', 'Autor', 'Valor', 'AdvogadoReu', 'AdvogadoAutor', 'DataAtualizacaoProcesso'])
        writer.writeheader()
        writer.writerows(finalJson)

    filepath_in = "Santander.txt"
    filepath_out = "Santander.xlsx"
    pd.read_csv(filepath_in, delimiter=',').to_excel(filepath_out)
