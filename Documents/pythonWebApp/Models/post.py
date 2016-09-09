import uuid
from database import Database

__author__ = 'Ian'


class Post(object):

    def __init__(self, blog_id, title, content, author, date, id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.id = uuid.uuid4().hex if id is None else id
        self.created_date = date

    def save_to_mongo(self):
        Database.insert(collection='posts',
                        data=self.json())

    def json(self):
        return {
            'id': self.id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
        }

    @staticmethod
    def from_mongo(id):
        data = Database.find_one(collection='posts',
                                 query={'id': id})

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id':id})]

