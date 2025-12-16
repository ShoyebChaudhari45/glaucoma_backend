from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
import gridfs

mongo = PyMongo()
jwt = JWTManager()


def init_extensions(app):
    mongo.init_app(app)
    jwt.init_app(app)


def get_fs():
    return gridfs.GridFS(mongo.db)
