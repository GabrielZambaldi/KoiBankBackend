from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'bancos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialize a instância db com o aplicativo Flask
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app, resources={r"/cadastrar": {"origins": "http://127.0.0.1:5501"}})

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

        # Retornar uma resposta em JSON com o ID atribuído e a mensagem de sucesso
        return jsonify({'id': novo_usuario.id, 'mensagem': 'Cadastro realizado com sucesso!'})

    except Exception as e:
        # Se ocorrer um erro, retorna uma mensagem de erro
        return jsonify({'erro': str(e)}), 500  # 500 é o código de status para erro interno do servidor

# Executar o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
