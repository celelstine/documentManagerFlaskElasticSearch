# documentManagerFlaskElasticSearch
`documentManagerFlaskElasticSearch` is a document management system implement in flask and powered by elasticsearch

# Installation
## Manual Installation
* clone the repo. 
* Create a virtual environment with python3 , check the file runtime.text.
* Ensure that you install and start [Elasticsearch](https://www.elastic.co/).
* Install dependencies --> `pip install -r requirements.txt`.
* Export your flask app, how ? `export FLASK_APP=app.py`.
* Then, run the project `python -m flask run`.
* The project uses jwt for authentication, ensure that you signup , then attach the jwt to subsequent request.

## Automated installation 
* Simply execute the startapp script as `sudo . startapp.sh` and follow the instructions.

#FAQ
* How do I change the index used in elasticsearch?
> The index can be alter easily, Configuration for this project are stored in a file **dochome/config**.
  To change the index used in elasticsearch change the value of **ES:index** node to a value that to you prefer
