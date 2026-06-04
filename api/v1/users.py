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

@user.route('/access/token')
@auth.login_required
def get_token():
    """
    User requests authentication token.

    Params:
    None
    """
    access_token = g.user.generate_auth_token()
    return { 'token': access_token }

@user.route('/users', methods=['GET'])
def users():
    """
    Queries database and retrieve all users in databases if any,
    error otherwise.
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

    Params
    Function takes in user id.
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

    Params
    None.
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

    Params
    user_id tied to the user.
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

@user.route('/update', methods=['UPDATE'])
@auth.login_required
def user_update():
    """
    Updates an exisiting user in the database.

    Params
    None.
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
