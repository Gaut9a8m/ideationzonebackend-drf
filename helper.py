import bcrypt, re
from ideationzone_backend.settings import SALT

# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), SALT)

# Check password
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


# validate email
def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    else:
        return False