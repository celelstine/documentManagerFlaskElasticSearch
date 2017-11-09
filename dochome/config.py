ES = {
  'index': 'dochome'
}

# app global secret
SUPER_SCERET = "themanisfalling4you!"

# setup elastic search
from elasticsearch import Elasticsearch
elasticsearch = Elasticsearch()

# list of unprotected routes
unprotectedRoutes =[
  '/login/',
  '/signup/'
]

