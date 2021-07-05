
const RequestSplit = ({spliter_result, hide_result}) => {
    
    return (
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
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    )}
                </div>                           
                <p className="font-semibold">{ (spliter_result.cumulative) ? spliter_result.cumulative : 0 }</p>
            </div>
            { spliter_result.requests && !hide_result && (
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

export default RequestSplit