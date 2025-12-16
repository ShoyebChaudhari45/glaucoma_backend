from extensions import mongo
from datetime import datetime

class UserModel:
    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def find_by_mobile(mobile):
        return mongo.db.users.find_one({"mobile": mobile})

    @staticmethod
    def create_user(name, email, mobile, dob, hashed_password):
        user = {
            "name": name,
            "email": email,
            "mobile": mobile,
            "dob": dob,
            "password": hashed_password,
            "created_at": datetime.utcnow()
        }
        mongo.db.users.insert_one(user)
        return user

    @staticmethod
    def delete_user(email):
        mongo.db.users.delete_one({"email": email})
