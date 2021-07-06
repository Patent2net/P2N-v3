import React from 'react';
import classnames from 'classnames';

const RequestList = ({ requestsEntries, setRequestsEntries, p2nAuto, setP2nAuto }) => {

    const changeEntryFromRequests = React.useCallback((value, index) => {
        console.log(value, index)
        setRequestsEntries((prevState ) => {
          const newState = [...prevState]
          newState[index] = value;
          return newState;
        })
    }, [setRequestsEntries])

    const deleteRequestRow = React.useCallback((index) => {
      setRequestsEntries((prevState ) => {
    
        const newState = [...prevState]
        if (newState.length > 1) {
          newState.splice(index, 1);
        }

        return newState;
      })
    }, [setRequestsEntries])

    const addRequestRow = React.useCallback((index) => {
      setRequestsEntries((prevState ) => {
    
        const newState = [...prevState]
        newState.push("")
        return newState;
      })
    }, [setRequestsEntries])

    return (
      <div>
        <p className="pb-2 text-sm text-gray-800">Enter in the textbox a valid espacenet smart search query for your patent research.</p>
        <div className="grid grid-cols-12">
          <div className="col-start-1 col-span-9">
            { requestsEntries.map((request, index) => (
              <div className="relative mb-2">
                <input
                  key={index}
                  value={request} 
                  onChange={(e) => changeEntryFromRequests(e.target.value, index)}
                  className="focus:shadow-outline px-3 py-3 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-base border border-blueGray-300 outline-none focus:outline-none focus:ring w-full"
                  type="text"
                  required={index === 0}
                  placeholder="Exemple: TA=lentille"
                  name="p2n_req"
                  id="p2n_reqBtn"
                />
                <div className={classnames("absolute top-0 bottom-0 right-0 pr-2 flex items-center", {
                  "hidden": requestsEntries.length === 1
                })}>
                  <button className="focus:shadow-outline focus:outline-none p-2 rounded-md font-semibold text-white cursor-pointer bg-gray-300 flex flex-row" onClick={() => deleteRequestRow(index)}>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            ))}
            {/* <div>
              <button className="focus:outline-none p-2 rounded-md text-sm font-semibold text-white cursor-pointer bg-red-500 flex flex-row" onClick={addRequestRow}>
                Ajouter une requête
              </button>
            </div> */}
            <button className="focus:shadow-outline focus:outline-none relative mb-2 cursor-pointer block w-full" onClick={addRequestRow}>
              <div className="text-center px-3 py-3 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-base border border-blueGray-300 outline-none focus:outline-none focus:ring w-full">
                <p>Ajouter une requête</p>
              </div>
            </button>
          </div>
        </div>
        <hr className="my-4" />
        <div>
          <div className="w-1/2 pt-2">
            <div 
              className={
                classnames(
                    "cursor-pointer box-border flex flex-col text-left border-2 text-sm", 
                    p2nAuto ? "rounded p-3 border-indigo-600 text-indigo-600" : "rounded p-3 opacity-30 opacity-50"
                )
              }
              onClick={() => setP2nAuto(!p2nAuto)}
            >
              <p className="font-medium text-indigo-600">Use auto request spliter</p>
              <p className="inline text-gray-800">
                It allows to exceed the limit of 2000 patents per request by splitting it into several sub-request
              </p>
            </div>
          </div>
        </div>
      </div>
    )

}

export default RequestList;