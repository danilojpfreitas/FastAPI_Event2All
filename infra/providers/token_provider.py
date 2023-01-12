from jose import jwt
from datetime import datetime, timedelta

# CONFIG
SECRET_KEY = 'a4bb06129dd888422a80bcf3a82dc9ee'
ALGORITHM = 'HS256'
EXPIRES_IN_INM = 3000


def new_access_token(data: dict):
    data = data.copy()
    time = datetime.utcnow() + timedelta(minutes=EXPIRES_IN_INM)

    data.update({'exp': time})

    token_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


def check_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('sub')


