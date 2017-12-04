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
  '/api/documents/',
  '/api/documents',
  '/api/document/<document_id>',
  '/api/search',
  '/api/search/<match_phrase>',
]

