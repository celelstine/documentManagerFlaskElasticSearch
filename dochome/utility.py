from .config import elasticsearch, ES, SUPER_SCERET
import bcrypt
import jwt
from flask_api import status

def user_exist(email):
    """
    Function to check if a user exist with the email address
    args: email (str)
    """
    es_result =  elasticsearch.search(
        index=ES.get('index'),
        doc_type='users',
        body= {
            "query": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "email.keyword": email
                            }
                        }
                    ]
                }
            }
        }
    )
    hits = es_result.get('hits')
    print(hits.get('total'))
    if hits.get('total') == 0:
        return False
    else:
        return hits.get('hits')

def toUnicode(input):
    """
    Convert bytes string to string
    """
    return str(input, 'utf-8')

def toBytesString(input):
    """
    Convert unicode string to bytes string
    """
    result = input.encode('latin-1')
    return result

def encryt(input):
    """
    Function to encrypt string using bcrypt and convert it to unicode
    args (str) input
    """
    input = toBytesString(input)
    result = bcrypt.hashpw(input, bcrypt.gensalt())
    return toUnicode(result)

def comparePassword(input, hash):
    """
    Function to compare password and hash
    """
    result = bcrypt.checkpw(toBytesString(input), toBytesString(hash))
    return result

def createJWt(payload):
    """
    Function to create jwt
    """
    encoded_jwt = jwt.encode(payload, SUPER_SCERET, algorithm='HS256')
    return encoded_jwt

def decodeJWT(token):
    """
    Function to decode jwt
    """
    payload = jwt.decode(token, SUPER_SCERET, algorithms=['HS256'])
    return payload


from flask import request

def islogin():
    token = request.headers.get('Authorization', None)

    try:
        payload = decodeJWT(token)
        return payload
    except:
        print('came here')
        return {'message': 'Authorized action, please login or signup'}, status.HTTP_401_UNAUTHORIZED
