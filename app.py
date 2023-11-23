from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Configuração do CORS

@app.route('/')
def index():
    return 'Bem-vindo ao backend do KoiBank!'

@app.route('/processar_formulario', methods=['POST'])
def processar_formulario():
    dados_do_formulario = request.get_json()
    # Lógica para processar os dados do formulário aqui
    print(dados_do_formulario)
    
    # Exemplo: Retornar uma resposta em JSON
    return jsonify({'mensagem': 'Formulário recebido com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)
