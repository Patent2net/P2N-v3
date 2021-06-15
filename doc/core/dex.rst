*******
P2N dex
*******

Generalities
============

dex.py is a script that allows to perform mutations on the local state of the application. It allows the user to be informed about the latest script execution and data modification.
The state is saved in json format in a file named dex.json

Dex format
==========

.. code-block:: json

    {
        "in_progress":[
        "jack"
        ],
        "done":[
        "lentille",
        "machinelearning"
        ],
        "requests":{
        "machinelearning":{
            "state":"SINGLE_REQ_WITH_SPLIT",
            "data":{
                "progress":{
                    "p2n_gather_biblio":{
                    "value":"100.00",
                    "max_value":"100"
                    },
                    "p2n_family":{
                    "value":"100.00",
                    "max_value":"100"
                    },
                    "...":{}
                },
                "to_be_found":{
                    "need_spliter":true,
                    "amount":10000,
                    "lstFicOk":[
                    
                    ]
                },
                "spliter_start_date":2021,
                "spliter_result":{
                    "start":true,
                    "requests":[
                    {
                        "name":"RequestsAuto/machinelearning/202101Request.cql",
                        "date":"2021",
                        "find":513
                    },
                    {
                        "name":"RequestsAuto/machinelearning/202102Request.cql",
                        "date":"2021",
                        "find":506
                    },
                    "..."
                    ],
                    "cumulative":2675,
                    "end":true
                },
                "process_list":{
                    "start":true,
                    "queue_list":[
                    "202101Request.cql",
                    "202102Request.cql",
                    "..."
                    ],
                    "done_list":[
                    "202101Request.cql",
                    "202102Request.cql",
                    "..."
                    ],
                    "end":true
                },
                "fusion_list":{
                    "start":true,
                    "queue_list":[
                    "machinelearning_segments_202101",
                    "machinelearning_segments_202102",
                    "..."
                    ],
                    "done_list":[
                    "machinelearning_segments_202101",
                    "machinelearning_segments_202102",
                    "..."
                    ],
                    "end":true
                }
            }
        },
        "lentille":{
            "state":"SINGLE_REQ_WITHOUT_SPLIT",
            "data":{
                "progress":{
                    "p2n_gather_biblio":{
                    "value":"100.00",
                    "max_value":"100"
                    },
                    "p2n_family":{
                    "value":"85.71",
                    "max_value":"100"
                    },
                    "...":{}
                }
            }
        }
        }
    }


Methods
=======

.. autofunction:: Patent2Net.app.dex.get_current_dex

State of a directory
--------------------

.. autofunction:: Patent2Net.app.dex.set_in_progress

.. autofunction:: Patent2Net.app.dex.set_done

.. autofunction:: Patent2Net.app.dex.set_state

.. autofunction:: Patent2Net.app.dex.get_state


Data linked to a directory
--------------------------

.. autofunction:: Patent2Net.app.dex.set_directory_request_data

.. autofunction:: Patent2Net.app.dex.get_directory_request_data

.. autofunction:: Patent2Net.app.dex.get_directory_request_data_all

.. autofunction:: Patent2Net.app.dex.delete_directory_request_data
