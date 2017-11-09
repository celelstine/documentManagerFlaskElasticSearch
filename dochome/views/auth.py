from flask_api import status
from flask import request
from datetime import datetime

from dochome.config import ES, elasticsearch
from dochome.utility import user_exist, encryt, toBytesString, toUnicode, comparePassword, createJWt
from app import app


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
	Route to login
	The request body should be of the format below
		{
			"email": <email_address>,
			"password": <your_password>
		}
	"""
    if request.method == 'POST':
        credential = request.data
        email = credential.get('email')
        password = credential.get('password')
        if email and password:
            try:
                es_result = user_exist(email)
                if es_result == False:
                    return "Wrong email or Password"
                record = es_result[0].get('_source')
                source_password = record.get('password')
                if comparePassword(password, source_password):
                    payload = {
                        "id": es_result[0].get('_id'),
                        "role": record.get('role_id')
                    }

                    response = {
                        "jwt": toUnicode(createJWt(payload)),
                        "name": record.get('name')
                    }
                    return response, status.HTTP_200_OK
                return {"message": "Wrong email or password"}, status.HTTP_400_BAD_REQUEST
            except Exception as ex:
                return {"message": "An error occurred, try again"}, status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Please attach your email and password"}, status.HTTP_400_BAD_REQUEST
    return {"message": "Use this route to login"}


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
	Route to signup
	The request body should be of the format:
		{
			"name": <firstname> <middlename> <lastname>,
			"email: <email>,
			"password: <your_password>
		}
	"""
    if request.method == "POST":
        credentails = request.data
        name = credentails.get('name', None)
        email = credentails.get('email', None)
        password = credentails.get('password', None)

        if name and email and password:
            # check if user exist
            userExist = user_exist(email)
            if userExist:
                return {"message": "An account with the email already exist"}, status.HTTP_400_BAD_REQUEST
            newUser = {
                'name': name,
                'email': email,
                'role_id': 1,
                'password': encryt(password)
            }
            try:
                es_result = elasticsearch.index(
                    index=ES.get('index'),
                    doc_type='users',
                    body=newUser
                )
                if es_result.get('result') == 'created':
                    payload = {
                        "id": es_result.get('id'),
                        "role": 1
                    }
                    response = {
                        "jwt": toUnicode(createJWt(payload)),
                        "message": "Welcome to Dochome, {}".format(newUser.get('name'))
                    }
                    return response, status.HTTP_201_CREATED
                return {"message": 'An error occurred, try again'}, status.HTTP_400_BAD_REQUEST
            except Exception as ex:
                return {"message": "An error occurred, try again"}, status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Please attach your email, name and password to the request"}, status.HTTP_400_BAD_REQUEST
    return {"message": "Use this route to signup"}
