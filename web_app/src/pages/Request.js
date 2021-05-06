import React from "react";
import { useHistory, useParams } from "react-router";
import { Link } from "react-router-dom";
import ProgressBar from "../components/ProgressBar";

const currentYear = new Date().getFullYear();
const years = Array.from({length: 30}, (_, i) => currentYear - i)

console.log(years)

const Show = () => {
    let { dir } = useParams();

    const [data, setData] = React.useState({});
    const [isViewUpdate, setIsViewUpdate] = React.useState(false);
    const [yearOpen, setYearOpen] = React.useState(false);
    const [year, setYear] = React.useState(currentYear)

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

    const onSelectYear = React.useCallback((year) => {
        setYear(year)
        setYearOpen(false)
    }, [setYear])

    const runSpliter = React.useCallback(() => {
        const data = new FormData();
        data.append("date", year);

        fetch('http://localhost:5000/api/v1/requests/' + dir + "/split", { 
            method: 'POST',
            body: data
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(json) {
            setIsViewUpdate(false)
        });             
    }, [year, dir])

    const isSpliterRun = React.useMemo(() => (
        data.state === "SPLITER_RUN"
    ), [data])

    const patentCount = React.useMemo(() => (
        isSpliterRun && data.data && !data.data.to_be_found
    ), [data, isSpliterRun])

    const patentCountResult = React.useMemo(() => (
        isSpliterRun && data.data && data.data.to_be_found
    ), [data, isSpliterRun])

    const requestSplit = React.useMemo(() => (
        isSpliterRun && data.data && data.data.split_result
    ), [data, isSpliterRun])



    const to_be_found = React.useMemo(() => patentCountResult && data.data.to_be_found, [data, patentCountResult])

    const split_result = React.useMemo(() => requestSplit && data.data.split_result, [data, requestSplit])    
    
    const to_be_found_amount = React.useMemo(() => (
        to_be_found && (to_be_found.amount >= 10000 ? `Plus de 10000` : to_be_found.amount)
    ), [to_be_found])

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
                                        { 
                                            data.done && (
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
                                            ) 
                                        }
                                        {
                                            !data.done && !isSpliterRun && (
                                                <div
                                                    className="focus:outline-none px-4 py-2 rounded-md font-semibold text-white bg-indigo-400 flex justify-center items-center"
                                                >
                                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                    </svg>
                                                    Chargements
                                                </div>
                                            )
                                        }

                                    </div>
                                </div>
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
                                            patentCount && (
                                                <div className="mt-4 p-4 border border-gray-200 flex flex-row justify-between rounded">
                                                    <p>Verification du nombre de ressource associé à la requete</p>
                                                    <div>
                                                        <svg className="animate-spin -ml-1 h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                                        </svg>
                                                    </div>
                                                </div>
                                            )
                                        }
                                        {
                                            patentCountResult && (
                                                <div className="mt-4 p-4 bg-indigo-600 flex flex-row justify-between rounded items-center text-white">
                                                    <div>
                                                        <p className="font-bold text-lg">{to_be_found_amount} éléments ont été trouvés</p>
                                                        <p className="text-sm">
                                                            {
                                                                to_be_found.need_spliter ?
                                                                "À partir de quelle année voulez vous récuperer les données ?" : 
                                                                "Il n'est pas necessaire de découper la requete, le traiement va bientôt commencer"
                                                            }
                                                        </p>
                                                    </div>
                                                    {
                                                        to_be_found.need_spliter && (
                                                            <div className="flex flex-row mt-1">
                                                                <div className="w-32">
                                                                    <div>
                                                                        <div className="relative text-black">
                                                                            <button type="button" className="relative w-full bg-white border border-gray-300 rounded-md shadow-sm pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 font-semibold" aria-haspopup="listbox" aria-expanded="true" aria-labelledby="listbox-label" onClick={() => setYearOpen(!yearOpen)}>
                                                                                <span className="flex items-center">
                                                                                    <span className="ml-3 block truncate">{ year }</span>
                                                                                </span>
                                                                                <span className="ml-3 absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                                                                                    <svg className="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                                                                    <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                                                                                    </svg>
                                                                                </span>
                                                                            </button>

                                                                            <ul style={{maxHeight: 200}} className={"absolute z-10 mt-2 w-full bg-white shadow-lg rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm" + (!yearOpen ? " transition ease-in duration-100 opacity-0" : " opacity-100")} tabindex="-1" role="listbox" aria-labelledby="listbox-label" aria-activedescendant="listbox-option-3">
                                                                            
                                                                                { years.map((year) => (
                                                                                    <li className="text-gray-900 cursor-default select-none relative py-2 pl-3 pr-9" id="listbox-option-0" role="option" onClick={() => onSelectYear(year)}>
                                                                                        <div className="flex items-center">
                                                                                    
                                                                                            <span className="font-normal ml-3 block truncate">
                                                                                                { year }
                                                                                            </span>
                                                                                        </div>
                                                                                    </li>
                                                                                ))}
                                                                            </ul>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <button type="button" className="bg-green-500 ml-2 px-2 rounded" aria-label="Suivant" onClick={() => runSpliter()}>
                                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                                                                    </svg>
                                                                </button>
                                                            </div>
                                                        )
                                                    }
                                                    
                                                </div>
                                            )
                                        }
                                        {
                                            requestSplit && (
                                                <p>Split result</p>
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

export default Show;