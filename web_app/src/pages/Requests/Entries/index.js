import React from "react";
import { useHistory } from "react-router";
import { Link } from "react-router-dom";

const entryTypes = {
  REQUEST: 'REQUEST',
  REQUESTS: 'REQUESTS',
  CSV: 'CSV'
}

function Entries({ entry, entryType, setEntry }) {

  const [ requestEntry, setRequestEntry] = React.useState("");
  const [ requestsEntry, setRequestsEntry ] = React.useState([""]);

  const changeEntryFromRequests = React.useCallback((value, index) => {
    console.log(value, index)
    setRequestsEntry((prevState ) => {

      const newState = [...prevState]
      newState[index] = value;

      if (value === '') {
        console.log("SLICE " + index )
        newState.splice(index, 1);
      }

      console.log(newState.length)
      if (newState.length <= index + 1) {
        newState.push("")
      }

      console.log(newState)

      return newState;
    })
  }, [setRequestsEntry])

  return (
    <div className="container mx-auto">


      { entryType === entryTypes.REQUEST && (
        <>
          <div class="mt-4">
            <label className="text-lg mb-2 font-bold">Request in CQL format</label>
            <p className="pt-2 pb-2 text-sm italic text-gray-800">Enter in the textbox a valid espacenet smart search query for your patent research.</p>
          </div>
          <div className="mb-2">
            <input
              value={entry} 
              onChange={(e) => setEntry(e.target.value)}
              className="px-3 py-4 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-base border border-blueGray-300 outline-none focus:outline-none focus:ring w-full"
              type="text"
              required
              placeholder="TA=lentille"
              name="p2n_req"
              id="p2n_reqBtn"
            />
          </div>
        </>
      )}

      { entryType === entryTypes.REQUESTS && (
        <>
          <div class="mt-4">
            <label className="text-lg mb-2 font-bold">Requests in CQL format</label>
            <p className="pt-2 pb-2 text-sm italic text-gray-800">
              Enter a list of valid espacenet search queries for your patent search in the text box.<br/>
              The results of all the queries will be combined into a single directory
            </p>
          </div>
          <div className="mb-2">
            {
              requestsEntry.map((request, index) => (
                <input
                  key={index}
                  value={request} 
                  onChange={(e) => changeEntryFromRequests(e.target.value, index)}
                  className="mb-2 px-3 py-4 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-base border border-blueGray-300 outline-none focus:outline-none focus:ring w-full"
                  type="text"
                  required
                  placeholder="TA=lentille"
                  name="p2n_req"
                  id="p2n_reqBtn"
                />
              ))
            }
          </div>
        </>
      )}

    </div>
  );
}

export default Entries;
