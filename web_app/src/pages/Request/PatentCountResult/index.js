import React from "react"

const currentYear = new Date().getFullYear();
const years = Array.from({length: 30}, (_, i) => currentYear - i)

const PatentCountResult = ({ dir, to_be_found }) => {

    const [yearOpen, setYearOpen] = React.useState(false);
    const [year, setYear] = React.useState(currentYear)

    const to_be_found_amount = React.useMemo(() => (
        to_be_found && (to_be_found.amount >= 10000 ? `Plus de 10000` : to_be_found.amount)
    ), [to_be_found])

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
        .then(function(json) {});
    }, [year, dir])

    const onSelectYear = React.useCallback((year) => {
        setYear(year)
        setYearOpen(false)
    }, [setYear])

    return (
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

export default PatentCountResult