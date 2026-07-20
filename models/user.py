from sqlalchemy import DateTime, Integer, Column, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models import Base
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

class User(Base, UserMixin):
    """
    Defines user class, str and methods for authentication
    mechanisms

    Params
    Inherits from Base and UserMixin for configs
    """

    __tablename__ = 'user_accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    username = Column(String(80))
    email = Column(String(120), unique=True, nullable=False)
    passwd_hash = Column(String(128), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # establish a relation between the user and expense table
    expenses = relationship('Expense', backref='user_accounts', lazy='dynamic')

    def generate_auth_token(self) -> str:
        """
        Generate an authentication token.

        Args:
            None

        Returns:
            Auth. token.
        """
        from app import app
        auth_s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return auth_s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(access_token, expires_in=3600):
        """
        Verifies authentication token.

        Params:
        :auth. token.
        """
        from models import app
        auth_s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            d = auth_s.loads(access_token, max_age=expires_in)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(d.get('id'))
        return user

    def __repr__(self) -> str:
        """
        Return a custom str representation of a user.

        Params:
        None.
        """
        return '{} - {}'.format(self.name, self.email)
    
    def to_dict(self) -> dict:
        """"
        Return a dictionary representation of user object for
        serialization.

        Params:
        None.
        """
        return dict(username=self.username,
                    email=self.email,
                    id=self.id,
                    created_at=self.created_at,
                    updated_at=self.updated_at
                )

    def hash_passwd(self, password: str) -> None:
        self.passwd_hash =  generate_password_hash(password)

    def verify_passwd(self, password: str) -> bool:
        return check_password_hash(self.passwd_hash, password)
