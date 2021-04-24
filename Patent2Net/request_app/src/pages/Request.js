import React from "react";
import { useHistory, useParams } from "react-router";
import ProgressBar from "../components/ProgressBar";

const Show = () => {
    let { dir } = useParams();

    const [data, setData] = React.useState({});

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
                        console.log("====>", key, eventData);
                        newData.progress[key] = eventData[key];
                    }
                    return newData;
                })
            }

        }
    }, [])

    console.log(data)

    return (
        <div className="container mx-auto">
            <div className="flex justify-center items-center">
                <div className="flex flex-col w-3/5 mt-24 mb-12 bg-white p-8 rounded shadow">
                    {
                        data.progress ? (
                            <>
                                <div class="pb-4">
                                    <h1 className="text-3xl font-semibold leading-7">{ dir }</h1>
                                    <h2 className="text-lg">{ data.cql && data.cql.requete }</h2>
                                </div>
                                <hr className="border-gray-200" />
                                <div class="pt-4">
                                    {Object.keys(data.progress).map((key, index) => (
                                        <ProgressBar 
                                            name={key}
                                            value={data.progress[key]["value"]}
                                            max_value={data.progress[key]["max_value"]}
                                        />
                                    ))}                 
                                </div>
                            </>
                        ) : null
                    }
                </div>   
            </div>
        </div>
    )   
}

export default Show;