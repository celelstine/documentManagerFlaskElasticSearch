from flask import Flask , request, render_template
from flask_api import FlaskAPI, status
from datetime import datetime

from flask_cors import CORS
from dochome.config import ES, elasticsearch
from dochome.utility import user_exist, encryt, toBytesString, toUnicode,comparePassword, createJWt


app = FlaskAPI(__name__, static_folder = "./dist/static", template_folder = "./dist")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

from dochome.views import * 

@app.route('/api')
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



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")