import bcrypt

from todoapp.domain.user.entities import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    def __init__(self, salt_rounds: int = 12):
        self.salt_rounds = salt_rounds

    def hash(self, password: str) -> str:
        salt = bcrypt.gensalt(self.salt_rounds)
        password = bcrypt.hashpw(password.encode(), salt)
        return password.decode()

    def verify(self, hashed_password: str, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())


