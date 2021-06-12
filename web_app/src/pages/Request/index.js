import React from "react";
import { useHistory, useParams } from "react-router";
import { Link } from "react-router-dom";
import FusionList from "./FusionList";
import RequestHeader from "./Header";
import PatentCount from "./PatentCount";
import PatentCountResult from "./PatentCountResult";
import ProcessList from "./ProcessList";
import Progress from "./Progress";
import RequestSplit from "./RequestSplit";


const Request = () => {
    let { dir } = useParams();

    const history = useHistory();
    const [data, setData] = React.useState({});

    const updateData = React.useCallback(() => {
        fetch("http://localhost:5000/api/v1/requests/" + dir)
        .then(function(response) {
            return response.json();
        })
        .then(function(json) {
            if(json.code === 200) {
                console.log(json.data)
                setData(json.data)
            }
        }).catch(() => {
            history.push('/app/requests')
        });
    }, [dir, history])
    
    React.useEffect(() => {
        updateData()
    }, [updateData]);

    React.useEffect(() => {
        console.log("Opening the SSE connection")
        var source = new EventSource("http://localhost:5000/api/v1/listen");
        source.onmessage = function(event) {
            const data = JSON.parse(event.data)
            console.log(data)
            if(data.data.directory === dir) {
                updateData()
            }
        }
        return () => {
            source.close()
        }
    }, [updateData, dir])
    
    const isSpliterRun = React.useMemo(() => (
        data.state === "SPLITER_RUN"
    ), [data])

    const showPatentCount = React.useMemo(() => (
        isSpliterRun && data.data && !data.data.to_be_found
    ), [data, isSpliterRun])

    const showRequestSplit = React.useMemo(() => (
        isSpliterRun && data.data && data.data.spliter_result
    ), [data, isSpliterRun])

    const showPatentCountResult = React.useMemo(() => (
        isSpliterRun && data.data && data.data.to_be_found && !showRequestSplit
    ), [data, isSpliterRun, showRequestSplit])

    const showProgressList = React.useMemo(() => (
        isSpliterRun && data.data && data.data.process_list
    ), [data, isSpliterRun])

    const showFusion = React.useMemo(() => (
        isSpliterRun && data.data && data.data.fusion_list
    ), [data, isSpliterRun])

    const to_be_found = React.useMemo(() => showPatentCountResult && data.data.to_be_found, [data, showPatentCountResult])

    const spliter_result = React.useMemo(() => showRequestSplit && data.data.spliter_result, [data, showRequestSplit])

    const process_list = React.useMemo(() => showProgressList && data.data.process_list, [data, showProgressList])

    const fusion_list = React.useMemo(() => showFusion && data.data.fusion_list, [data, showFusion])

    const showRequestProgress = React.useMemo(() => (
        showFusion && fusion_list.end
    ), [showFusion, fusion_list])

    return (
        <div className="container mx-auto">
            <div className="flex justify-center items-center">
                <div className="flex flex-col w-full lg:w-3/5 mb-12 bg-white p-8 rounded shadow">
                    {
                        data.cql ? (
                            <>
                                <RequestHeader dir={dir} data={data} showLoading={!isSpliterRun} />
                                <hr className="border-gray-200" />
                                {
                                    !isSpliterRun ? 
                                    (
                                        <>
                                            <Progress data={data} />
                                        </>
                                    ) : (
                                        <>
                                        {
                                            showPatentCount && ( <PatentCount /> )
                                        }
                                        {
                                            showPatentCountResult && ( <PatentCountResult dir={dir} to_be_found={to_be_found} /> )
                                        }
                                        {
                                            showRequestSplit && ( <RequestSplit spliter_result={spliter_result} hide_result={showProgressList} /> )
                                        }
                                        {
                                            showProgressList && ( <ProcessList process_list={process_list} hide_result={showFusion}/> )
                                        }
                                        {
                                            showFusion && ( <FusionList fusion_list={fusion_list} /> )
                                        }
                                        {
                                            showRequestProgress && ( <Progress data={data} /> )
                                        }
                                        </>
                                    )
                                }
                                
                            </>
                        ) : null
                    }
                </div>   
            </div>
        </div>
    )   
}

export default Request;