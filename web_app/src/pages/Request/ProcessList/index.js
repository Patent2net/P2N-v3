
const ProcessList = ({ process_list, hide_result }) => (
    <div className="mt-4 p-4 border border-gray-200 rounded">
        <div className="flex flex-row justify-between items-center">
            <p className="font-semibold mr-3">
                { (!process_list.start && !process_list.end) && "Gathering will start soon" }
                { (process_list.start && !process_list.end) && "Gatherers are running" }
                { (process_list.end) && "Process is finished" }
            </p>
            { !process_list.end && (
                <svg className="animate-spin -ml-1 h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
            )}
        </div>
        
        {
            !hide_result && (
                <>
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
                </>
            )
        }
        
        
    </div>
)



export default ProcessList