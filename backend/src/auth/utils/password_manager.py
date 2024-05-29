import ast
from bcrypt import hashpw, gensalt, checkpw


async def get_hashed_password(password: str):
    return hashpw(password.encode('utf-8'), gensalt())

async def verify_password(password: str, current_hashed_password: str) -> bool:
    current_hashed_password_bytes = ast.literal_eval(current_hashed_password)
    return checkpw(password.encode('utf-8'), current_hashed_password_bytes)

async def validate_password(password: str) -> bool:
    return len(password) >= 6