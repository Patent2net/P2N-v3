import React from "react";
import { useHistory, useParams } from "react-router";
import { Link } from "react-router-dom";
import ProgressBar from "../../components/ProgressBar";
import RequestHeader from "./Header";
import PatentCount from "./PatentCount";
import PatentCountResult from "./PatentCountResult";


const Request = () => {
    let { dir } = useParams();

    const [data, setData] = React.useState({});

    const updateData = React.useCallback(() => {
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
    }, [dir])
    
    React.useEffect(() => {
        updateData()
    }, [updateData]);

    React.useEffect(() => {
        console.log("Opening the SSE connection")
        var source = new EventSource("http://localhost:5000/api/v1/listen");
        source.onmessage = function(event) {
            const data = JSON.parse(event.data)
            console.log(data)
            if(data.data.directory === dir) {
                updateData()
            }
        }
        return () => {
            source.close()
        }
    }, [updateData, dir])
    
    const isSpliterRun = React.useMemo(() => (
        data.state === "SPLITER_RUN"
    ), [data])

    const patentCount = React.useMemo(() => (
        isSpliterRun && data.data && !data.data.to_be_found
    ), [data, isSpliterRun])

    const requestSplit = React.useMemo(() => (
        isSpliterRun && data.data && data.data.spliter_result
    ), [data, isSpliterRun])

    const patentCountResult = React.useMemo(() => (
        isSpliterRun && data.data && data.data.to_be_found && !requestSplit
    ), [data, isSpliterRun, requestSplit])


    const to_be_found = React.useMemo(() => patentCountResult && data.data.to_be_found, [data, patentCountResult])

    const spliter_result = React.useMemo(() => requestSplit && data.data.spliter_result, [data, requestSplit])    
    

    return (
        <div className="container mx-auto">
            <div className="flex justify-center items-center">
                <div className="flex flex-col w-full lg:w-3/5 mb-12 bg-white p-8 rounded shadow">
                    {
                        data.cql ? (
                            <>
                                <RequestHeader dir={dir} data={data} showLoading={!isSpliterRun} />
                                <hr className="border-gray-200" />
                                {
                                    !isSpliterRun ? 
                                    (
                                        <>
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
                                                <div className="mt-4 p-4 border border-gray-200">
                                                    <p>La requete est terminé</p>
                                                </div>
                                            )
                                        }
                                        </>
                                    ) : (
                                        <>
                                        {
                                            patentCount && ( <PatentCount /> )
                                        }
                                        {
                                            patentCountResult && ( <PatentCountResult dir={dir} to_be_found={to_be_found} /> )
                                        }
                                        {
                                            requestSplit && (
                                                <div className="mt-4 p-4 border border-gray-200 rounded">
                                                    <div className="flex flex-row justify-between">
                                                        <div className="flex flex-row justify-between items-center">
                                                            <p className="font-semibold mr-3">
                                                                { (!spliter_result.start && !spliter_result.end) && "La séparation de la requete va commencer" }
                                                                { (spliter_result.start && !spliter_result.end) && "Séparation de la requete en cours" }
                                                                { (spliter_result.end) && "La séparation de la requete est terminé" }

                                                            </p>
                                                            { !spliter_result.end && (
                                                                <svg className="animate-spin -ml-1 h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                                </svg>
                                                            )}
                                                        </div>                           
                                                        <p className="font-semibold">{ (spliter_result.cumulative) ? spliter_result.cumulative : 0 }</p>
                                                    </div>
                                                    { spliter_result.requests && (
                                                        <>
                                                            <hr className="border-gray-200 my-4" />
                                                            <div>
                                                                { spliter_result.requests && spliter_result.requests.map((request) => (
                                                                    <div className="flex flex-row justify-between">
                                                                        <p>{request.name}</p>
                                                                        <p>{request.find}</p>
                                                                    </div>
                                                                ))}
                                                            </div>
                                                        </>
                                                    )}

                                                </div>
                                            )
                                        }
                                        </>
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

export default Request;