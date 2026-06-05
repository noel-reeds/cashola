from flask import Flask
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
    swagger.config['title'] = 'Cash0la API'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.url_map.strict_slashes = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
 
    from api.v1.auth import auth as auth_blueprint
    from api.v1.expenses import expense as expense_blueprint
    from api.v1.users import user as users_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')
    app.register_blueprint(expense_blueprint, url_prefix='/api/v1')
    app.register_blueprint(users_blueprint, url_prefix='/api/v1')
    return app

app = setup()

if __name__ == "__main__":
    app.run(port=8000, debug=True)
