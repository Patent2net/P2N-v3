import React from "react";
import { useHistory, useParams } from "react-router";
import { Link } from "react-router-dom";
import ProgressBar from "../../components/ProgressBar";
import RequestHeader from "./Header";
import PatentCount from "./PatentCount";
import PatentCountResult from "./PatentCountResult";
import RequestSplit from "./RequestSplit";


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
            updateData()
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

    const is_process_list = React.useMemo(() => (
        isSpliterRun && data.data && data.data.process_list
    ), [data, isSpliterRun])


    const to_be_found = React.useMemo(() => patentCountResult && data.data.to_be_found, [data, patentCountResult])

    const spliter_result = React.useMemo(() => requestSplit && data.data.spliter_result, [data, requestSplit])

    const process_list = React.useMemo(() => is_process_list && data.data.process_list, [data, is_process_list])

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
                                            requestSplit && ( <RequestSplit spliter_result={spliter_result} hide_result={process_list} /> )
                                        }
                                        {
                                            is_process_list && (
                                                <div className="mt-4 p-4 border border-gray-200 rounded">
                                                    <div className="flex flex-row justify-between items-center">
                                                        <p className="font-semibold mr-3">
                                                            { (!process_list.start && !process_list.end) && "La récuperation des données va commencer" }
                                                            { (process_list.start && !process_list.end) && "Les données sont en cours de récupération" }
                                                            { (process_list.end) && "La récupération des données est terminé" }
                                                        </p>
                                                        { !process_list.end && (
                                                            <svg className="animate-spin -ml-1 h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                            </svg>
                                                        )}
                                                    </div>
                                                    
                                                    <hr className="border-gray-200 my-4" />
                                                    <div>
                                                        { process_list.queue_list && process_list.queue_list.map((file) => (
                                                            <div className="flex flex-row justify-between">
                                                                <p>{file}</p>
                                                                <div>
                                                                    {
                                                                        process_list.done_list.includes(file) && (
                                                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                                                            </svg>
                                                                        )
                                                                    }
                                                                </div>
                                                            </div>
                                                        ))}
                                                    </div>
                                                   
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