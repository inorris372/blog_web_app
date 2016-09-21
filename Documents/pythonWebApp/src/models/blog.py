import datetime
import uuid
from src.common.database import Database
from src.models.post import Post

__author__ = 'Ian'


class Blog(object):
    def __init__(self, author, author_id, title, description, identity=None):
        self.author = author
        self.title = title
        self.description = description
        self.identity = uuid.uuid4().hex if identity is None else identity
        self.author_id = author_id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        post = Post(blog_id=self.identity,
               title=title,
               content=content,
               author =self.author,
               created_date=date)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self.identity)

    def save_to_mongo(self):
        Database.insert(collection='blogs',
                        data=self.json())

    def json(self):
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'identity': self.identity
        }

    @classmethod
    def from_mongo(cls, identity):
        blog_data = Database.find_one(collection='blogs',
                                      query={'identity': identity})
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blogs',
                              query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]
