from passlib.context import CryptContext


class PasswordHasher:
    _context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

    def hash(self, password: str) -> str:
        return self._context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self._context.verify(plain_password, hashed_password)