from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from aplicacion import config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import  Api
from aplicacion.schemas import Usuariosschema, Partidosschema, Partidoschema, Equiposschema

app = Flask(__name__)
app.config.from_object(config)
cors = CORS(app, resources={r"/apiCampeonato/*": {"origins": "http://localhost:3000"}})
db = SQLAlchemy(app)
api = Api(app)


api.add_resource(Usuariosschema,"/apiCampeonato/users","/apiCampeonato/users/login","/apiCampeonato/users/register")
api.add_resource(Partidosschema,"/apiCampeonato/matches","/apiCampeonato/matches/<idPartido>")
api.add_resource(Partidoschema,"/apiCampeonato/matchById/<idMatch>")
api.add_resource(Equiposschema,"/apiCampeonato/teams")
