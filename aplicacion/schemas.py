from flask_restful import Resource
from flask import request, jsonify
from sqlalchemy import delete, null
import jwt
import datetime
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        from aplicacion.index import app
        from aplicacion.models import Usuarios as us
        token = None
       
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'No ha enviado un token valido', "Statuscode":401})
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"],algorithms=["HS256"])
            current_user = us.query.filter_by(id=data['public_id']).first()
        except:
            return jsonify({'message': 'token es invalido',"Statuscode":401})
        if not current_user:
            return jsonify({'message': 'token es invalido', "Statuscode":401})
        return f(current_user,**kwargs)
    return decorator


class Usuariosschema(Resource):

    def get(self):
        auth = request.authorization   
        from aplicacion.models import Usuarios as us
        from aplicacion.index import app
        if not auth or not auth.username or not auth.password:  
            return {"message":"Faltan datos, Debe loguearse"},401    

        user = us.query.filter_by(username=auth.username).first()   

        if user is not None:
            if user.password == auth.password:  
                token = jwt.encode({'public_id': user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
                return jsonify({"token" :  token})

        return {"message":"Datos incorrectos, debe loguearse"},401
 
    def post(self):
        data = request.get_json()
        from aplicacion.index import db
        from aplicacion.models import Usuarios as us
        user = us.query.filter_by(username=data['username']).first()
        if user is None:
            user = us(nombre=data['nombre'], correo=data['correo'], username=data['username'],password=data['password'])
            db.session.add(user)
            db.session.commit()
            return {"message":"Usuario creado con Exito"},200
        else:
            return {"Error":"El username que intenta registrar se encuentra registrado"},401


class Partidosschema(Resource):
    @token_required
    def get(self):
        from aplicacion.models import Partidos as part
        from aplicacion.models import Usuarios as us
        from aplicacion.models import Equipos as eq
        data = []
        partidos = part.query.all()
        for partido in partidos:
            user =  us.query.get(partido.usuario)
            visitante = eq.query.get(partido.visitante)
            local = eq.query.get(partido.local)
            data.append({
                "id":partido.id,
                "usuario":{
                    "id":user.id,
                    "username":user.username,
                    "nombre":user.nombre,
                    "correo":user.correo
                },
                "local":{
                    "id":local.id,
                    "nombre":local.nombre
                    },
                "visitante":{
                    "id":visitante.id,
                    "nombre":visitante.nombre
                    },
                "fecha":f"{partido.fecha}",
                "goleslocal":partido.goles_local,
                "golesvisitante":partido.goles_visitante
            })
        return {"data":data}

    @token_required
    def post(self):
        data = request.get_json()
        from aplicacion.index import db
        from aplicacion.models import Partidos as part
        partido = part(usuario=data['usuario'], local=data['local'], visitante=data['visitante'],fecha=data['fecha'])
        db.session.add(partido)
        db.session.commit()
        return {"message":"Partido creado con exito"},200

    @token_required
    def put(self,idPartido):
        from aplicacion.models import Partidos as part
        from aplicacion.index import db
        data = request.get_json()
        partido = part.query.get(idPartido)

        if partido is not None:
            partido.goles_local = data["goleslocal"]
            partido.goles_visitante = data["golesvisitante"]
            db.session.add(partido)
            db.session.commit()
            return {"message":"Partido actualizado con exito"}
        else:
            return {"Error":"Dato no actualizado, ya que no se encontro en almacenamiento."},404



