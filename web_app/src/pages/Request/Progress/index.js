import ProgressBar from "../../../components/ProgressBar";

const progress_lang = {
    "p2n_req": "Gathering patent list",
    "p2n_family": "Gathering patent family",
    "p2n_gather_biblio": "Gathering patent metadata",
    "p2n_content": "Gathering patent content",
    "p2n_image": "Gathering patent content",
    "p2n_network": "Patent network",
    "p2n_tables": "Patent tables",
    "p2n_carrot": "Patent carrot",
    "p2n_iramuteq": "Patent iramuteq",
    "p2n_cluster": "Patent cluster",
}

const Progress = ({ data }) => (
    <div className="mt-4 p-4 border border-gray-200 rounded">
        <div className="flex flex-row justify-between items-center">
            {
                (!data.done) && (
                    <p className="font-semibold mr-3">
                        { (!data.progress) && "La requete va bientôt se lancer" }
                        { (data.progress) && "La requete est en cours" }
                    </p>
                )
            }
            { (data.done) && (
                <div className="flex-1">
                    <p className="font-semibold mr-3">La requete est terminé</p>
                    {/* <ul className="mt-2 flex flex-col w-100">
                        { Object.keys(data.cql.options).map((key) => {
                            const option = data.cql.options[key];
                            console.log(option)

                            return (
                                <li className="flex-1 flex justify-between" key={key}>
                                    <span>{key}</span>
                                    <span>{option ? (
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                        </svg>
                                    ) : (
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                        </svg>
                                    )}</span>
                                </li>
                            )
                        })}
                    </ul> */}
                </div>
            )}
            { !data.done && (
                <svg className="animate-spin -ml-1 h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
            )}
        </div>
        {
            (data.done === false && data.progress && (
                <>
                    <hr className="border-gray-200 my-4" />
                    <div>
                        {Object.keys(data.progress).map((key, index) => (
                            <ProgressBar
                                key={key}
                                name={progress_lang[key] || key}
                                value={data.progress[key]["value"]}
                                max_value={data.progress[key]["max_value"]}
                        />
                        ))}                 
                    </div>
                </>
            ))
        }
    </div>
)

export default Progress