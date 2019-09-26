from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

# from seguranca import authenticate, identity

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.secret_key = 'herverson'
api = Api(app)

# jwt = JWT(app, authenticate, identity)

receitas = []

class Receita(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('preco',
        type=float,
        required=True,
        help="Esse campo não pode estar vazio!"
    )

    def get(self, nome):
        return {'receita': next(filter(lambda x: x['nome'] == nome, receitas), None)}

    def post(self, nome):
        if next(filter(lambda x: x['nome'] == nome, receitas), None) is not None:
            return {'menssagem': "essa receita '{}' já existe.".format(nome)}

        data = Receita.parser.parse_args()

        receita = {'nome': nome, 'preco': data['preco']}
        receitas.append(receita)
        return receita

    def delete(self, nome):
        global receitas
        receitas = list(filter(lambda x: x['nome'] != nome, receitas))
        return {'mensagem': 'Receita deletada'}

    def put(self, nome):
        data = Receita.parser.parse_args()
        receita = next(filter(lambda x: x['nome'] == nome, receitas), None)
        if receita is None:
            receita = {'nome': nome, 'preco': data['preco']}
            receitas.append(receita)
        else:
            receita.update(data)
        return receita

class ListaReceita(Resource):
    def get(self):
        return {'receitas': receitas}

api.add_resource(Receita, '/receita/<string:nome>')
api.add_resource(ListaReceita, '/receitas')

if __name__ == '__main__':
    app.run(debug=True) 