import ProgressBar from "../../../components/ProgressBar";

const Progress = ({ data }) => (
    <div className="mt-4 p-4 border border-gray-200 rounded">
        <div className="flex flex-row justify-between items-center">
            <p className="font-semibold mr-3">
                { (!data.progress && !data.done) && "La requete va bientôt se lancer" }
                { (data.progress && !data.done) && "La requete est en cours" }
                { (data.done) && "La requete est terminé" }
            </p>
            { !data.done && (
                <svg className="animate-spin -ml-1 h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
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
                                name={key}
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