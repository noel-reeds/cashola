from flask import Blueprint, jsonify, g, request
from werkzeug.security import generate_password_hash
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

user = Blueprint('user', __name__)

@auth.verify_password
def verify_password(username_or_token, password):
    """
    Verifies a user before accessing protected or private
    endpoints.

    Params
    Username and password of user.
    """
    from models import User
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_passwd(password):
            return False
    g.user = user
    return True

@user.route("/", methods=['GET'])
def root_URL():
    """
    Tests status of API
    """
    return {'status': 'OK!'}

@user.route('/access/token')
@auth.login_required
def get_token():
    """
    User requests authentication token.
    ---
    tags:
        - Auth
    responses:
        200:
            description: return an auth token.
        404:
            description: an error occured.
    params:
        description: None
    """
    access_token = g.user.generate_auth_token()
    return { 'token': access_token }

@user.route('/users', methods=['GET'])
def users():
    """
    Queries database and retrieve all users in databases if any, error otherwise.
    ---
    tags:
        - Users
    responses:
        200:
            description: List of users.
        404:
            description: No users found.
    """
    from models import User, session
    try:
        users = session.query(User).all()
        if users:
            return {"users": [user.to_dict() for user in users]}
        else:
            return {'message':'no users'}
    except Exception as err:
        return {'message':'{}'.format(err)}

@user.route('/user/<int:user_id>', methods=['GET'])
async def specific_user(user_id):
    """
    Returns a user specified by user_id if present, error otherwise.
    ---
    tags:
        - Users
    responses:
        200:
            description: A user specified with user_id.
        404:
            description: No user found.
    params:
        description: user_id
    """
    from models import User
    # check for a user matching the supplied id
    try:
        user = User.query.filter_by(id=user_id).first()
        return user.to_dict()
    except Exception as e:
        return {'message':'user does not exist'}

@user.route('/signup', methods=['POST'])
async def create_user():
    """
    Creates and persists a new user to the database.
    If user already exists, return an error.
    ---
    tags:
        - Users
    responses:
        200:
            description: user creates, OK!
        404:
            description: error with the request.
    params:
        description: None.
    """
    from models import User, session
    try:
        if request.is_json:
            user_creds = request.json
            password = user_creds.get("password")
        new_user = User(email=user_creds.get('email'),
                        username=user_creds.get('username'),
                        name=user_creds.get('name')
                    )
        email=user_creds.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'message': 'user already exists'})
        new_user.hash_passwd(password)
        session.add(new_user)
        session.commit()
        return jsonify({'message': 'OK'})
    except Exception as e:
        print(e)
        return jsonify({'message':'an error with the request'})

@user.route('/delete_a_user/<int:user_id>', methods=['DELETE'])
async def delete_a_user(user_id):
    """
    Deletes a user if present in database, returns an error
    otherwise.
    ---
    tags:
        - Users
    responses:
        200:
            description: user deleted, OK!
        404:
            description: user does not exist.
    params:
        description: user_id tied to the user.
    """
    from models import User, session
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return {"status": "OK"}
        return {"message": "user does not exist!"}
    except Exception as e:
        return {"message": "An error with the request!"}

@user.route('/update', methods=['PATCH'])
@auth.login_required
def user_update():
    """
    Updates an exisiting user in the database.
    ---
    tags:
        - Users
    responses:
        200:
            description: user update, OK!
        400:
            description: an error occured.
    params:
        description: None.
    """
    from models import User, session
    try:
        if not request.is_json:
            raise Exception
        updated = request.json
        password = updated.get("password")
        if password is not None:
            pwd_hash = generate_password_hash(password)
            [updated.pop(k, None) for k in ['password', 'id']]
            updated.update(passwd_hash=pwd_hash)
            session.query(User).filter(User.id == g.user.id).update(updated)
            session.commit()
            return {"message": "OK"}
        else:
            session.query(User).filter(User.id == g.user.id).update(updated)
            session.commit()
            return {"message": "OK"}
    except Exception as e:
        return {"message": "FAILED"}
