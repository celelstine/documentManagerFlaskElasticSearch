from flask_api import status
from flask import request
from datetime import datetime

from dochome.config import ES, elasticsearch, unprotectedRoutes
from dochome.utility import user_exist, encryt, toBytesString, toUnicode,comparePassword, createJWt, islogin, decodeJWT
from app import app


@app.before_request
def before_request():
    """
    A middleware for every route, it checks for jwt for protected routes
    :returns: (json) jwy payload
    """
    rule = request.url_rule
    try:
        if rule.rule not in unprotectedRoutes:
            token = request.headers.get('Authorization', None)

            try:
                global user_payload
                user_payload = decodeJWT(token)
            except:
                return {'message': 'Authorized action, please login or signup'}, status.HTTP_401_UNAUTHORIZED
    except:
        return { "message": "we do not support the route or method, please review the endpoint"}, status.HTTP_400_BAD_REQUEST

@app.route('/documents/', methods=['GET', "POST"])
@app.route('/documents', methods=['GET', "POST"])
def getDocuments():
    """
    Route to get all at least 10 documents or created a name documents

    .. note::

        This route is accessible to only authenticated uses
        you can .. _login: /login or .. _sign: /signup

    :returns:

        .. topic:: Route Description
            For GET request: (json) documents -- list of documents

                example:
                .. code-block:: json

                    {
                        "documents": [
                            {
                                "owner": "AV-ZwBhvMzTJYPRr5QNw",
                                "body": "Imagine cars running on glass tyres, that is a minimist picture of our world with the greatest and the forgiver",
                                "title": "What is life without grace and love",
                                "accessRight": "Public",
                                "accessGroup": null,
                                "id": "AV-b5rc55h_O6rfBmbtK"
                            },
                            {
                                "owner": "AV-ZwBhvMzTJYPRr5QNw",
                                "body": "God is indeed great ans merciful",
                                "title": "God is great",
                                "accessRight": "Public",
                                "accessGroup": null,
                                "id": "AV-aza795h_O6rfBmbtI"
                            }
                        ]
                    }
                OR

                 .. code-block:: json

                    { "message": "You have no document, you can create one now."}

            For POST request : (json) message -- a description of the status of the opereation

            .. note::  The request should be have the structure below:

                 .. code-block:: json

                    {
                        "title": "<document_title>", # compulsory
                        "body": "<document_body", # compulsory
                        "accessRight" : <"such as private, public or group: default is public"> ,
                    }
    """
    if request.method == "GET":
        user_id = user_payload.get("id")
        user_role = user_payload.get("role")
        page_no = request.args.get('page', 0)
        size = request.args.get('size', 10)
        startIndex = (size * page_no) - size

        if startIndex < 1:
            startIndex = 0

        if page_no == 0:
            page_no = 1

        es_result = elasticsearch.search(
            index=ES.get('index'),
            doc_type='documents',
            body={
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    "doc_status": "active"
                                }
                            },
                            {
                                "bool": {
                                    "should": [
                                        {
                                            "term": {
                                                "accessRight": "public"
                                            }
                                        },
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "accessRight.keyword": "Role"
                                                        }
                                                    },
                                                    {
                                                        "term": {
                                                            "accessGroup": user_role
                                                        }
                                                    }
                                                ]
                                            }
                                        },
                                        {
                                            "term": {
                                                "owner": user_id
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }

                },
                "from": startIndex, "size": size  # for pagination
            }
        )
        hits = es_result.get('hits')
        count = hits.get('total')
        if count > 0:
            documents = []
            for document in hits.get('hits'):
                curdoc = document.get("_source")
                # attach the document id
                curdoc['id'] = document.get("_id")
                documents.append(curdoc)
            return { "documents": documents, "total": count, "current_page": page_no }, status.HTTP_200_OK
        return { "message": "You have no document, you can create one now."}, status.HTTP_200_OK

    if request.method == "POST":
        request_body = request.data
        body = request_body.get("body")
        title =  request_body.get("title")

        if body and title:
            owner = user_payload.get("id")
            user_role = user_payload.get("role")
            accessRight = request_body.get('accessRight', "Public")

            accessGroup = None

            if accessRight not in ['Role', 'Public', 'Private']:
                return { "message": "Invalid access rigth, choose one from thes options [ 'Role', 'Public', 'Private']"}, status.HTTP_400_BAD_REQUEST
            if accessRight in ['role', 'Role']:
                accessGroup = user_role

            newDocument = {
                "owner": owner,
                "body": body,
                "title": title,
                "accessRight": accessRight,
                "accessGroup": accessGroup,
                "doc_status": "active"
            }

            try:
                es_result = elasticsearch.index(
                    index=ES.get('index'),
                    doc_type='documents',
                    body=newDocument
                )

                if es_result.get('result') == 'created':
                    response = {
                        "message": "The document: {} has been created successfully".format(title)
                    }
                    return response, status.HTTP_201_CREATED

                return {"message": 'An error occurred, try again'}, status.HTTP_400_BAD_REQUEST
            except Exception as ex:
                return {"message": "An error occurred, try again"}, status.HTTP_500_INTERNAL_SERVER_ERROR
        return { "message": "Please attach the document's body and title"}, status.HTTP_400_BAD_REQUEST
    return { "message": "God is merciful"}


@app.route('/document/<document_id>', methods = ["GET", "PUT", "DELETE" ])
def document(document_id):
    """
    Route to get, update or delete an document
    :param document_id: the id of the doucment
    .. note::

        This route is accessible to only authenticated uses
        you can .. _login: /login or .. _sign: /signup

    :returns:

        .. topic:: Route Description
            For GET request: (json) documents -- the document

                example:
                .. code-block:: json


                    {
                        "owner": "AV-ZwBhvMzTJYPRr5QNw",
                        "body": "Imagine cars running on glass tyres, that is a minimist picture of our world with the greatest and the forgiver",
                        "title": "What is life without grace and love",
                        "accessRight": "Public",
                        "accessGroup": null,
                        "id": "AV-b5rc55h_O6rfBmbtK"
                    }

                OR

                 .. code-block:: json

                    { "message": "The document does not exist, please confirm  that the id is correct."}

            For UPDATE request : (json) message -- a description of the status of the opereation

            .. note::  The request should be have the structure below:

                 .. code-block:: json

                    {
                        "title": "<document_title>", # compulsory
                        "body": "<document_body", # compulsory
                        "accessRight" : <"such as private, public or group: default is public"> ,
                    }

            For DELETE request : (json) message -- a description of the status of the opereation

    """

    found_document = {}
    try:
        es_result = elasticsearch.get(
            index=ES.get('index'),
            doc_type='documents',
            id=document_id,
            ignore=[404]
        )
        found = es_result.get('found')

        if found == False or es_result.get('_source').get('doc_status') != 'active':
            return { "message": "The document does not exist, please confirm  that the id is correct."}, status.HTTP_200_OK

        user_id = user_payload.get("id")
        user_role = user_payload.get("role")
        found_document = es_result.get('_source')

        if request.method == "GET":
            can_view_doc = True
            if found_document.get('accessRight') == 'Private' and found_document.get('owner') == user_id:
                can_view_doc =  False
            elif found_document.get('accessRight') == 'Role' and found_document.get('accessGroup') == user_role:
                can_view_doc = False
            else:
                can_view_doc = True

            # a user can view documents that he created but shared in the role that is that her present role
            if found_document.get('owner') == user_id:
                can_view_doc =  True

            if can_view_doc == False:
                return {"message": "Unauthorized operation"}, status.HTTP_401_UNAUTHORIZED

            found_document['id'] = document_id
            return { "document": found_document }, status.HTTP_200_OK

        if request.method  == "PUT":
            if found_document.get('owner') == user_id:
                request_body = request.data
                accessRight = request_body.get('accessRight', found_document.get('accessRight'))
                title = request_body.get('title', found_document.get('title'))
                body =   request_body.get('body', found_document.get('body'))
                accessGroup = None

                if accessRight not in ['Role', 'Public', 'Private']:
                    return { "message": "Invalid access rigth, choose one from thes options [ 'Role', 'Public', 'Private']"}, status.HTTP_400_BAD_REQUEST

                if accessRight in ['role', 'Role']:
                    accessGroup = user_role

                update_document = {
                    "owner": user_id,
                    "body": body,
                    "title": title,
                    "accessRight": accessRight,
                    "accessGroup": accessGroup
                }

                es_script = ""
                for key, value in update_document.items():
                    if key != 'accessGroup':
                        es_script += "ctx._source.{} = '{}';".format(key, value)
                    else:
                        es_script += "ctx._source.{} = {};".format(key, value)

                es_result = elasticsearch.update(
                    index=ES.get('index'),
                    doc_type='documents',
                    id=document_id,
                    body= {"script": es_script}
                )

                if es_result.get('result') == 'updated':
                    return  {"message": "Document has been succesfully updated"}, status.HTTP_200_OK
                return {"message": "Unable to update this document, please try again . Send us a mail if this error persist (okorocelestine@gmail.com)"}, status.HTTP_200_OK
            return {"message": "Unauthorized operation"}, status.HTTP_401_UNAUTHORIZED

        if request.method == "DELETE":

            if found_document.get("owner") == user_id:
                # es_result = elasticsearch.delete (
                #     index=ES.get('index'),
                #     doc_type='documents',
                #     id=document_id
                # )

                es_result = elasticsearch.update(
                    index=ES.get('index'),
                    doc_type='documents',
                    id=document_id,
                    body={"script": "ctx._source.doc_status = 'deleted';"}
                )
                print(es_result)
                if es_result.get('result') == 'updated':
                    return {"message": "Document has been succesfully deleted"}, status.HTTP_200_OK
                return {"message": "Unable to delete this document, please try again . Send us a mail if this error persist (okorocelestine@gmail.com)"}, status.HTTP_200_OK
            return { "message": "Unauthorized operation"}, status.HTTP_401_UNAUTHORIZED
    except Exception as ex:
        # todo: We need to keep trace of this error, logging this error would achieve that.
        return { "message": "An error occurred, please try again . Send us a mail if this error persist (okorocelestine@gmail.com)"}, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/search', methods=['GET'])
@app.route('/search/<match_phrase>', methods=['GET'])
def search(match_phrase=None):
    """
    Route to search for documents that contains the phrase passed in it's body or title
    :return:

        .. topic:: Route Description
                For GET request: (json) documents -- list of documents with highlight of the phrase

                    example: response from the endpoint search/e or search/q=e
                    .. code-block:: json

                        {
                            "documents":[
                                {
                                    "_index": "dochome",
                                    "_type": "documents",
                                    "_id": "AV-etjVP5h_O6rfBmbtW",
                                    "_score": 0.3666863,
                                    "_source": {
                                        "owner": "AV-ZwBhvMzTJYPRr5QNw",
                                        "body": "I give myself away, here I am Lord",
                                        "title": "Total surrender",
                                        "accessRight": "Public",
                                        "accessGroup": null,
                                        "doc_status": "active"
                                    },
                                    "highlight": {
                                        "body": [
                                            "<em>I</em> give myself away, here <em>I</em> am Lord"
                                        ]
                                    }
                                },
                                {
                                    "_index": "dochome",
                                    "_type": "documents",
                                    "_id": "AV-esAwB5h_O6rfBmbtT",
                                    "_score": 0.26301134,
                                    "_source": {
                                        "owner": "AV-ZwBhvMzTJYPRr5QNw",
                                        "body": "Imagine life without grace, we have a God would love without limits. I love him so much",
                                        "title": "God is mercy and gracious",
                                        "accessRight": "Role",
                                        "accessGroup": 1,
                                        "doc_status": "deleted"
                                    },
                                    "highlight": {
                                        "body": [
                                            "Imagine life without grace, we have a God would love without limits. <em>I</em> love him so much"
                                        ]
                                    }
                                }
                            ]
                        }
                    OR

                     .. code-block:: json

                        { "message": "You have no document, you can create one now."}
    """
    if request.method == "GET":
        phrase = request.args.get('q', match_phrase)
        page_no = request.args.get('page', 0)
        size = request.args.get('size', 10)
        startIndex = (size * page_no) - size

        if startIndex < 1:
            startIndex = 0

        if page_no == 0:
            page_no = 1

        if phrase is None:
            return {"message": "You need to specific the search phrase, attach it like this ?q=<love>"}, status.HTTP_400_BAD_REQUEST

        user_id = user_payload.get("id")
        user_role = user_payload.get("role")

        query_body = {
            "query": {
                "bool":{
                    "must": [
                        {
                            "term": {
                                "doc_status": "active"
                            }
                        },
                        {
                            "bool": {
                                "should": [
                                    {
                                        "match_phrase": {
                                            "title": phrase
                                        }
                                    },
                                    {
                                        "match_phrase": {
                                            "body": phrase
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "bool": {
                                "should": [
                                    {
                                        "term": {
                                            "accessRight": "public"
                                        }
                                    },
                                    {
                                        "bool": {
                                            "must": [
                                                {
                                                    "term": {
                                                        "accessRight.keyword": "Role"
                                                    }
                                                },
                                                {
                                                    "term": {
                                                        "accessGroup": user_role
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        "term": {
                                            "owner": user_id
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            "highlight": {
                "fields": {
                    "title": {},
                    "body": {}
                }
            },
            "from": startIndex, "size": size  # for pagination
        }

        es_result = elasticsearch.search(
            index=ES.get('index'),
            doc_type='documents',
            body=query_body
        )
        hits = es_result.get('hits')
        count = hits.get('total')
        if count > 0:
            documents = []
            for document in hits.get('hits'):
                curdoc = document.get("_source")
                # attach the document id
                curdoc['id'] = document.get("_id")
                curdoc = {
                    "document": curdoc,
                    "highlight": document.get("highlight")
                }
                documents.append(curdoc)
            return {"documents": documents, "total": count, "current_page": page_no}, status.HTTP_200_OK
        return {"message": "You have no document, you can create one now."}, status.HTTP_200_OK