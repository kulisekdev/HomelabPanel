from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
import argon2

ph = PasswordHasher()

def hash_password(password: str):
    if password:
        try:
            hashedPass = ph.hash(password)
            return {
                "msg": "Successfully hashed password.",
                "result": hashedPass,
                "success": True
            }
        except Exception as e:
            return {
                "msg": f"Error: {e}",
                "success": False
            }

def verify_hashed_password(hashed_password: str, password: str) -> bool:
    if password:
        try:
            ph.verify(hashed_password, password)
            return True
        except VerifyMismatchError:
            return False
        except VerificationError:
            return False