from flask_script import Manager
from aplicacion.index import app

manager = Manager(app)
app.config['DEBUG'] = True

if __name__ == "__main__":
    manager.run()