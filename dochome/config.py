ES = {
  'index': 'dochome'
}

# app global secret
SUPER_SCERET = "themanisfalling4you!"

# setup elastic search
from elasticsearch import Elasticsearch
elasticsearch = Elasticsearch()

# list of unprotected routes
protectedRoutes =[
  '/documents/',
  '/documents',
  '/document/<document_id>',
  '/search',
  '/search/<match_phrase>',
]

