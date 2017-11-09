# documentManagerFlaskElasticSearch
A document management system implement in flask and powered by elasticsearch

# Installation
    * clone the repo.
    * Create a virtual environment with python3 , check the file runtime.text.
    * Ensure that you install and start [Elasticsearch](https://www.elastic.co/).
    * Install dependencies --> `pip install -r requirements.txt`.
    * Export your flask app, how ? `export FLASK_APP=app.py`.
    * Then, run the project `python -m flask run`.
    * The project uses jwt for authentication, ensure that you signup , then attach the jwt to subsequent request
