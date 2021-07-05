import React from "react"

const Home = ({version}) => {

    const [isUpdate, setIsUpdate] = React.useState(false)

    const update = React.useCallback(() => {
        setIsUpdate(true)
        fetch("http://localhost:5000/updateP2N")
        .then(function(response) {
            setIsUpdate(false)
        })
    }, [])

    return (
        <div className="container mx-auto">
            <div className="flex justify-center items-center">
                <div className="flex flex-col w-full lg:w-3/5 mb-12 bg-white p-8 rounded shadow">
                    <h1 className="text-4xl font-semibold mb-2 text-gray-900">Patent2Net Docker Version : <span className="font-normal">{version}</span> </h1>
                    <hr />
                    <div className="mt-4">
                        <div className="mt-4">
                            <p className="text-gray-800 text-sm mb-4 text-justify">Patent2Net is a toolkit for patent information processing and statistical analysis for education and science.<br/>
                            Patent2Net helps to collect, study and analyze patent data from the European Patent Office’s Open Patent Services API (OPS). <br/>
                            Patent2Net is a free software dedicated to :
                            </p>	
                            
                            <ul className="list-disc text-gray-800 text-sm mb-3 text-justify">
                                <li>provide statistical analysis and representations of a set of patents.</li>
                                <li>promote the use of patent information in the academic field, nano and small firms,
                                developing countries.</li>
                                <li>study and practice how to collect, treat and communicate “textual bibliographic information”
                                and learn the automation process.</li>
                            </ul>
                            
                            <p className="text-gray-800 text-sm mb-4 text-justify">Contributions are always welcome!
                            </p>
                        </div>
                    </div>
                    <hr/>
                    <div className="mt-4">
                        <p className="text-gray-800 text-sm mb-4 text-justify">To update your P2N version click on the button : </p>
                        <button onClick={update} className="w-64 focus:outline-none px-8 py-2 rounded-md font-semibold text-white bg-red-500 cursor-pointer mt-4 flex flex-ror justify-center items-center">
                            Update P2N
                            {
                                isUpdate && (
                                    <svg className="animate-spin ml-1 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                )
                            }
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Home