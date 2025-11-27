import bcrypt

class PasswordManager:
    @staticmethod
    def hash(pwd: str):
        return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify(pwd: str, hashed: str):
        return bcrypt.checkpw(pwd.encode(), hashed.encode())
