import bcrypt
from models.user_model import UserModel


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


def signup_user(name, email, mobile, dob, password):
    if UserModel.find_by_email(email):
        raise ValueError("Email already registered")

    if UserModel.find_by_mobile(mobile):
        raise ValueError("Mobile number already registered")

    hashed_password = hash_password(password)

    UserModel.create_user(
        name=name,
        email=email,
        mobile=mobile,
        dob=dob,
        hashed_password=hashed_password
    )


def login_user(email: str, password: str):
    user = UserModel.find_by_email(email)
    if not user:
        raise ValueError("Invalid credentials")

    if not check_password(password, user["password"]):
        raise ValueError("Invalid credentials")

    return user
