from flask import Flask , request
from flask_api import FlaskAPI, status
from datetime import datetime

from dochome.config import ES, elasticsearch
from dochome.utility import user_exist, encryt, toBytesString, toUnicode,comparePassword, createJWt


app = FlaskAPI('dochome')

from dochome.views import * 

@app.route('/')
def index():
	newUser = {
		'name': 'Okoro Celestine',
		'email': 'okorocelestine@gmail.com',
		'role_id': 1,
		'password': encryt('smilesh2o')
	}
	try:
		es_result = elasticsearch.index(
			index=ES.get('index'),
			doc_type='users',
			id=1,
			body=newUser
		)
		if es_result.get('result') == 'created':
			print(es_result)
			return 'Welcome to Dochome, {}.'.format(newUser.get('name'))
		else:
			return 'An error occurred, try again'
	except Exception as ex:
		return 'an error occurred, trace: {}'. format(str(ex))


