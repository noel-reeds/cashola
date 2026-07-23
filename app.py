from flask import Flask, redirect
from flasgger import Swagger
from dotenv import load_dotenv
import os

load_dotenv()

def setup() -> Flask:
    """
    setup() -> Flask
    Instantiate a Flask app, configures with the database engine,
    sessions with flask_login and
    registers views blueprints

    Params:
    Function takes no parameters.
 
    Returns a flask app instance.
    """
    app = Flask(__name__)
    swagger = Swagger(app)
    swagger.config['title'] = 'Skrilla API'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.url_map.strict_slashes = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
 
    from api.v1.auth import auth as auth_blueprint
    from api.v1.expenses import expense as expense_blueprint
    from api.v1.users import user as users_blueprint
    
    @app.route("/", methods=['GET'])
    def root_URL():
        """
        Tests status of API
        """
        return redirect('https://cashola.onrender.com/apidocs/', code=302)

    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')
    app.register_blueprint(expense_blueprint, url_prefix='/api/v1')
    app.register_blueprint(users_blueprint, url_prefix='/api/v1')
    return app

app = setup()

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
