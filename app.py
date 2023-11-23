from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Configuração do CORS

@app.route('/')
def index():
    return 'Bem-vindo ao backend do KoiBankss!'

@app.route('/processar_formulario', methods=['POST'])
def processar_formulario():
    try:
        dados_do_formulario = request.get_json()
        # Lógica para processar os dados do formulário aqui
        print(dados_do_formulario)
        
        # Exemplo: Retornar uma resposta em JSON
        return jsonify({'mensagem': 'Formulário recebido com sucesso!'})

    except Exception as e:
        # Se ocorrer um erro, retorna uma mensagem de erro
        return jsonify({'erro': str(e)}), 500  # 500 é o código de status para erro interno do servidor

if __name__ == '__main__':
    app.run(debug=True)
