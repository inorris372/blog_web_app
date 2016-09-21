import uuid
from flask import session
from src.common.database import Database
from src.models.blog import Blog

__author__ = 'Ian'


class User(object):
    def __init__(self, email, password, identity=None):
        self.email = email
        self.password = password
        self.identity = uuid.uuid4().hex if identity is None else identity

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, identity):
        data = Database.find_one("users", {"identity": identity})
        if data is not None:
            return cls(**data)

    @staticmethod
    def has_registered(email):
        user = User.get_by_email(email)
        if user is not None:
            return True
        return False

    @staticmethod
    def login_valid(email, password):
        # Check whether a user's email matches the password they sent us
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        # login_valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self.identity)

    def new_blog(self, title, description):
        # author, title, description, author_id
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self.identity)

        blog.save_to_mongo()

    def json(self):
        return {
            "email": self.email,
            "identity": self.identity,
            "password": self.password
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())
