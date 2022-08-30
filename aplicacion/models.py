from sqlalchemy import BigInteger, Column, Integer, Date, String,ForeignKey
from sqlalchemy.orm import relationship
from aplicacion.index import db


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id =  Column(BigInteger,primary_key=True,autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(50), nullable=False)
    username = Column(String(10), nullable=False)
    password = Column(String(10), nullable=False)
    partidos = relationship("Partidos", cascade ="all, delete-orphan", backref="Usuarios",lazy=True)


class Partidos(db.Model):
    __tablename__ = 'partidos'
    id =  Column(BigInteger,primary_key=True,autoincrement=True)
    usuario = Column(BigInteger,ForeignKey('usuarios.id'),nullable=False)
    local = Column(BigInteger,ForeignKey('equipos.id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    visitante = Column(BigInteger,ForeignKey('equipos.id',ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    fecha = Column(Date, nullable=False)
    goles_local = Column(Integer,nullable=True)
    goles_visitante = Column(Integer,nullable=True)

class Equipos(db.Model):
    __tablename__ = 'equipos'
    id =  Column(BigInteger,primary_key=True,autoincrement=True)
    nombre = Column(String(20), nullable=False)
    partidos = relationship('Equipos', secondary='partidos', secondaryjoin=Partidos.visitante==id, primaryjoin=Partidos.local==id)