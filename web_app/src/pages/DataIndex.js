import React from "react";
import { Link } from "react-router-dom";

const DataIndex = () => {
    const [ requests, setRequests ] = React.useState({});
  
    React.useEffect(() => {
        fetch("http://localhost:5000/api/v1/requests")
        .then(function(response) {
            return response.json();
        })
        .then(function(json) {
          if (json.data) {
            setRequests(json.data)
          }
          console.log(json.data)
        });
    }, []);
    
    return (
        <div className="container mx-auto">
            <div className="flex justify-center items-center">
                <div className="flex flex-col w-full lg:w-3/5 mb-12 bg-white p-8 rounded shadow">
                    <div>
                        <h1 className="text-3xl font-semibold mb-2 text-gray-900">Index</h1>
                        <hr/>
                        
                        <div className="mt-4">
                            { requests.done && requests.done.map((name) => (
                                <div key={name}>
                                    <a rel="noreferrer" target="_blank" href={"http://localhost:5000/DATA/" + name + ".html" } >{name}</a>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default DataIndex