from flask import Flask, render_template, request, make_response
import pandas as pd
import numpy as np
import time
app = Flask(__name__)
base = pd.read_csv('base_lista.csv').set_index(['org', 'dest'])
print('base de dados carregada')
app.config['MAX_CONTENT_PATH'] = 100000

@app.route('/distancias')
def upload_file():
    return render_template('upload.html')

# @app.route('/erro')
# def error_upload_file():
#     return render_template('erro.html')

@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        #ler base de dados
        f = request.files['file']
        # ler aquivo do usuário via post
        try:
            print('iniciando leitura do arquivo')
            consulta = pd.read_csv(f, sep=',', decimal='.', engine='c', dtype= np.int64).dropna(how='any')
            print('arquivo lido')
            # consulta = consulta.astype(np.int64)
            # print('cod convertidos para inteiros')
        except:
            erro = "ERRO NA LEITURA DO ARQUIVO: Todos os pares org-dest devem ser números inteiros, de acordo com a lista de municípios do IBGE. Certifique-se que o arquivo .csv não contém texto, como #N/A ou #VALUE"
            return render_template('upload.html',erro=erro)

        consulta = consulta.set_index(['org', 'dest'])
        if len(consulta.index) <= 200000: 
            print('realizando busca na base')
            retorno = consulta.join(base, how='left')
            print('base terminada')
        if len(consulta.index) > 200000: 
            erro = "ERRO: A base de entrada deve ter no máximo 200k linhas."
            return render_template('upload.html',erro=erro)

        resp = make_response(retorno.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=distancias.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
    app.debug = True

