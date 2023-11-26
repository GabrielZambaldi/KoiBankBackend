from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
CORS(app)

app = Flask(__name__)
CORS(app, resources={r"/login": {"origins": "http://127.0.0.1:5501"}})  # Ajuste a rota conforme necessário

# Configuração do banco de dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'bancos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialize a instância db com o aplicativo Flask
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Defina seu modelo de usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primeiro_nome = db.Column(db.String(100))
    ultimo_nome = db.Column(db.String(100))
    cpf = db.Column(db.String(15), unique=True)
    senha = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, primeiro_nome, ultimo_nome, cpf, senha, email):
        self.primeiro_nome = primeiro_nome
        self.ultimo_nome = ultimo_nome
        self.cpf = cpf
        self.senha = senha
        self.email = email

# Crie as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Esquema de marshmallow para serialização
class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'primeiro_nome', 'ultimo_nome', 'cpf', 'senha', 'email')

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

# Rota para cadastrar um novo usuário
@app.route('/cadastrar', methods=['POST'])
@cross_origin()
def cadastrar():
    try:
        dados_do_formulario = request.get_json()

        # Verifique se o CPF já está em uso
        if Usuario.query.filter_by(cpf=dados_do_formulario['cpf']).first():
            return jsonify({'erro': 'CPF já cadastrado'}), 400  # 400 é o código de status para solicitação inválida

        # Crie um novo objeto Usuario a partir dos dados do formulário
        novo_usuario = Usuario(
            primeiro_nome=dados_do_formulario['primeiroNome'],
            ultimo_nome=dados_do_formulario['ultimoNome'],
            cpf=dados_do_formulario['cpf'],
            senha=dados_do_formulario['senha'],
            email=dados_do_formulario['email'],
        )

        # Adicione o novo usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()

        # Exemplo: Retornar uma resposta em JSON com o ID atribuído
        return jsonify({'id': novo_usuario.id, 'mensagem': 'Cadastro realizado com sucesso!'})

    except Exception as e:
        # Se ocorrer um erro, retorna uma mensagem de erro
        return jsonify({'erro': str(e)}), 500  # 500 é o código de status para erro interno do servidor

# Rota para fazer login
@cross_origin()
@app.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5501")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response
    elif request.method == 'POST':
        try:
            dados_do_formulario = request.get_json()

            # Verifique se o usuário com o CPF e senha fornecidos existe no banco de dados
            usuario = Usuario.query.filter_by(cpf=dados_do_formulario['cpf'], senha=dados_do_formulario['senha']).first()

            if usuario:
                return jsonify({'mensagem': 'Login bem-sucedido!', 'id_usuario': usuario.id})
            else:
                return jsonify({'erro': 'Credenciais incorretas'}), 401

        except Exception as e:
            return jsonify({'erro': str(e)}), 500

# Rota para obter mensagens personalizadas com base no ID do usuário
@app.route('/mensagens/<int:id_usuario>', methods=['GET'])
@cross_origin()
def obter_mensagens_personalizadas(id_usuario):
    # Lógica para obter mensagens personalizadas com base no id_usuario
    # Por enquanto, retornaremos uma mensagem fixa como exemplo
    return jsonify({'mensagem_personalizada': f'Olá, usuário {id_usuario}! Bem-vindo de volta!'})

if __name__ == '__main__':
    app.run(debug=True)
