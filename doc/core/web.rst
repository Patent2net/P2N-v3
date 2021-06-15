*****************
P2N web interface
*****************

Generalities
============

The patent2net web interface allows queries to be made directly from the web browser.
It is available at the url http://localhost:5000/app


How it works
============

The web interface is developed with the react framework. The sources are available in the *web_app* directory
To work, the application uses a web api.

Web API
=======

.. http:get:: /api/v1/requests

    Retrieves the list of current requests

    **Example request**:

    .. http:example:: curl wget httpie python-requests

        GET /api/v1/requests HTTP/1.1
        Host: localhost:5000

    **Example response**:

    .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "code":200,
                "message":"",
                "data":{
                    "done":[
                        "lentille"
                    ],
                    "in_progress":[
                        "machinelearning"
                    ],
                    "global_progress":{
                        "machinelearning":{
                            "done_step_count":8,
                            "progress_step_count":2,
                            "total_step_count":10
                        }
                    }
                }
            }



    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: error

.. http:post:: /api/v1/requests

    Allows you to create a new request

    **Example request**:

    .. http:example:: curl wget httpie python-requests

        POST /api/v1/requests HTTP/1.1
        Host: localhost:5000
        Content-Type: application/x-www-form-urlencoded

        p2n_dir=lentille&p2n_req=TA=lentille&p2n_options=p2n_family,p2n_image,p2n_network,p2n_bibfile


    **Example response**:

    .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "code": 200,
                "message": "Spliter start",
                "data": {
                    "p2n_dir": "lentille"
                }
            }


    :query string p2n_dir: name of the target directory
    :query string p2n_req: cql request
    :query string p2n_options: active treatment options
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: error


.. http:get:: /api/v1/requests/(string:p2n_dir)

    Is used to retrieve data from a request directory (`p2n_dir`)

    **Example request**:

    .. http:example:: curl wget httpie python-requests

        GET /api/v1/requests/lentille HTTP/1.1
        Host: localhost:5000

    **Example response**:

    .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "code": 200,
                "message": "",
                "data": {
                    "done": true,
                    "state": "SINGLE_REQ_WITHOUT_SPLIT",
                    "data": {
                        "progress": {
                            "p2n_gather_biblio": {
                                "value": "100.00",
                                "max_value": "100"
                            },
                            "p2n_family": {
                                "value": null,
                                "max_value": null
                            },
                            "...": {},
                        }
                    },
                    "directory": "lentille",
                    "cql": {
                        "requete": "TA=lentille",
                        "ndf": "lentille",
                        "options": {
                            "GatherContent": true,
                            "GatherBiblio": true,
                            "GatherPatent": true,
                            "GatherFamilly": true
                        }
                    }
                }
            }

    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: error

.. http:post:: /api/v1/requests/(string:p2n_dir)/split

    Allows you to start trimming a query that exceeds the limit of 2000 patents in a certain year. The splitting will not start if the patents count is not finished

    **Example request**:

    .. http:example:: curl wget httpie python-requests

        POST /api/v1/requests/autom/split HTTP/1.1
        Host: localhost:5000
        Content-Type: application/x-www-form-urlencoded

        date=2020

    **Example response**:

    .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "code": 200,
                "message": "Spliter running",
                "data": {}
            }

    :query int date: Start date of the splitting process
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: error

.. http:post:: /api/v1/requests/(string:p2n_dir)/interface

    Allows to rebuild the interface of a data directory (`p2n_dir`)

    **Example request**:

    .. http:example:: curl wget httpie python-requests

        POST /api/v1/requests/lentille/interface HTTP/1.1
        Host: localhost:5000

    **Example response**:

    .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "code": 200,
                "message": "OK",
                "data": {
                    "directory": "lentille"
                }
            }

    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: error


Event systeme
=============