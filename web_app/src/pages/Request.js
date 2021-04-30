import React from "react";
import { useHistory, useParams } from "react-router";
import { Link } from "react-router-dom";
import ProgressBar from "../components/ProgressBar";

const Show = () => {
    let { dir } = useParams();

    const [data, setData] = React.useState({});
    const [isViewUpdate, setIsViewUpdate] = React.useState(false);

    React.useEffect(() => {
        fetch("http://localhost:5000/api/v1/requests/" + dir)
        .then(function(response) {
            return response.json();
        })
        .then(function(json) {
            if(json.code === 200) {
                console.log(json.data)
                setData(json.data)
            }
        });
    }, [dir]);

    React.useEffect(() => {
        console.log("Opening the SSE connection")
        var source = new EventSource("http://localhost:5000/listen");
        source.onmessage = function(event) {
            const received = JSON.parse(event.data)
            console.log(received)

            if (received.data) {
                const eventData = received.data

                setData((data) => {
                    const newData = {...data};
                    for(let key in eventData) {
                        if (newData.progress) {
                            console.log("====>", key, eventData);
                            newData.progress[key] = eventData[key];
                        }
                    }
                    return newData;
                })
            }
        }

        return () => {
            source.close()
        }
    }, [])

    const updateView = React.useCallback(() => {
        setIsViewUpdate(true)
        fetch('http://localhost:5000/api/v1/requests/' + dir + "/interface", { 
            method: 'POST'
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(json) {
            setIsViewUpdate(false)
        });
    }, [dir])


    return (
        <div className="container mx-auto">
            <div className="flex justify-center items-center">
                <div className="flex flex-col w-3/5 mb-12 bg-white p-8 rounded shadow">
                    {
                        data.cql ? (
                            <>
                                <div className="pb-4 flex justify-between">
                                    <div className="flex items-center">
                                        <Link 
                                            to={"/app/requests" }
                                            className="focus:outline-none p-2 rounded-md font-semibold text-white bg-gray-600"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                                            </svg>
                                        </Link>
                                        <div className="ml-4">
                                            <h1 className="text-3xl font-semibold leading-7">{ dir }</h1>
                                            <h2 className="text-lg">{ data.cql && data.cql.requete }</h2>
                                        </div>
                                    </div>
                                    <div className="flex items-center">
                                        { data.done ? (
                                            <>
                                                <button 
                                                    className="focus:outline-none p-2 rounded-md font-semibold text-white bg-red-500 mr-2 flex justify-center items-center"
                                                    onClick={updateView}
                                                >
                                                    {
                                                        isViewUpdate ? (
                                                            <svg className="animate-spin h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                            </svg>
                                                        ) : (
                                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                                            </svg>
                                                        )
                                                    }
                                                </button>
                                                <a 
                                                    target="_blank"
                                                    rel="noreferrer"
                                                    href={"/DATA/" + dir + ".html"} 
                                                    className="focus:outline-none px-8 py-2 rounded-md font-semibold text-white bg-indigo-500"
                                                >
                                                    Voir les données
                                                </a>
                                            </>
                                        ) : (
                                            <div
                                                className="focus:outline-none px-4 py-2 rounded-md font-semibold text-white bg-indigo-400 flex justify-center items-center"
                                            >
                                                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                </svg>
                                                Chargements
                                            </div>
                                        )}

                                    </div>
                                </div>
                                <hr className="border-gray-200" />
                                {
                                    (data.done === false && data.progress && (
                                        <div class="pt-4">
                                            {Object.keys(data.progress).map((key, index) => (
                                                <ProgressBar
                                                    key={key}
                                                    name={key}
                                                    value={data.progress[key]["value"]}
                                                    max_value={data.progress[key]["max_value"]}
                                            />
                                            ))}                 
                                        </div>
                                    )) || (
                                        <div className="pt-4">
                                            <p>La requete est terminé</p>
                                        </div>
                                    )
                                }
                            </>
                        ) : null
                    }
                </div>   
            </div>
        </div>
    )   
}

export default Show;