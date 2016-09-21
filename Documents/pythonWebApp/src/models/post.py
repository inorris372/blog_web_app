import datetime
import uuid

from src.common.database import Database
import src.models.blog

__author__ = 'Ian'


class Post(object):

    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), identity=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.identity = uuid.uuid4().hex if identity is None else identity
        self.created_date = created_date

    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        blog = src.models.blog.Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)

    def json(self):
        return {
            'identity': self.identity,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, identity):
        post_data = Database.find_one(collection='posts', query={'identity': identity})
        return cls(**post_data)

    @staticmethod
    def from_blog(identity):
        return [post for post in Database.find(collection='posts', query={'blog_id': identity})]
