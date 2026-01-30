import uuid
from typing import Any
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from diskcache import Cache

class AuthService:
    def __init__(self, cache: Cache):
        self.cache = cache
        self.hasher = PasswordHasher()

    def password_encode(self, password: str) -> str:
        return self.hasher.hash(password)

    def password_verify(self, hash_str: str | None, password: str) -> bool:
        try:
            if not hash_str: return False
            self.hasher.verify(hash_str, password)
            return True
        except VerifyMismatchError:
            return False

    def create_session(self, user_id: str) -> str:
        session_id = str(uuid.uuid4())
        self.cache.set(session_id, user_id, expire=60 * 60 * 24 * 28)
        return session_id

    def delete_session(self, session_id: str) -> None:
        if session_id: self.cache.delete(session_id)

    def delete_all_session(self, user_id: str) -> None:
        for session_id in self.cache.iterkeys():
            if self.cache.get(session_id) == user_id:
                self.cache.delete(session_id)

    def get_user_id(self, session_id: str) -> tuple[str | Any]:
        return self.cache.get(session_id)
