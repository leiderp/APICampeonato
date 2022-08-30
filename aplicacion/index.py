from flask import Flask, request, jsonify, make_response
from aplicacion import config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import  Api
from aplicacion.schemas import Usuariosschema, Partidosschema

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
api = Api(app)

api.add_resource(Usuariosschema,"/users","/users/login","/users/register")
api.add_resource(Partidosschema,"/matches","/matches/<idPartido>")
#@app.route("/")
#def inicio():
 #   from aplicacion.models import Usuarios as us
    #user = us(nombre="Leider",correo="leiderp@gmail.com",username="leiderp",password="12345")
    #db.session.add(user)
    #db.session.commit()
  #  datos = us.query.all()
   # data = {}
    #for dat in datos:
     #   data[dat.id] = [dat.nombre,dat.correo]
    #return make_response(jsonify({"data": data}))
