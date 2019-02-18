import json
from csv import DictWriter
import pandas as pd


def Export(jsonToExport):
    with open(jsonToExport, "r") as f:
        fileJson = json.load(f)

    for item in fileJson['Recovery']:
        fileJson['Recovery'][item]['CNJ'] = item

    finalJson = []

    for item in fileJson['Recovery']:
        finalJson.append(fileJson['Recovery'][item])

    with open('Recovery.txt', 'w', encoding='UTF-8') as outfile:
        writer = DictWriter(outfile, delimiter=',', lineterminator='\n', fieldnames=[
                            'CNJ', 'descricao', 'data', "CPFCNPJ", "Tipo", 'Decisao', 'Onus', 'Forum', 'TipoProcesso', 'Vara', 'Reu', 'Autor', 'Valor', 'AdvogadoReu', 'AdvogadoAutor', 'DataAtualizacaoProcesso'])
        writer.writeheader()
        writer.writerows(finalJson)

    filepath_in = "Recovery.txt"
    filepath_out = "Recovery.xlsx"
    pd.read_csv(filepath_in, delimiter=',').to_excel(filepath_out)
