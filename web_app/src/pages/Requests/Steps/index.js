import React from 'react';
import { useHistory } from 'react-router-dom';
import uploadFilesService from '../../../services/upload-files.service';
import Step from '../Step';
import Upload from '../Upload';
import ChooseLocation from './ChooseLocation';
import ChooseOptions from './ChooseOptions';
import ChooseRequestType from './ChooseRequestType/index.js';
import RequestList from './RequestList';

const Steps = () => {

    const history = useHistory();

    const [focusID, setFocusID] = React.useState(0);
    const [requestType, setRequestType] = React.useState('request');

    const [csvUploadInfo, setCsvUploadInfo] = React.useState();
    const [selectedFile, setSelectedFile] = React.useState();
    const [selectedHeader, setSelectedHeader] = React.useState();
    const [directory, setDirectory] = React.useState("");
    const [safeDirectory, setSafeDirectory] = React.useState("");
    const [options, setOptions] = React.useState([
        "p2n_content",
        "p2n_gather_biblio",
        "p2n_family",
        "p2n_image",
        "p2n_network",
        "p2n_freeplane",
        "p2n_bibfile",
        "p2n_map",
        "p2n_tables",
        "p2n_carrot",
        "p2n_iramuteq",
        "p2n_cluster",
    ]);

    const [ requestsEntries, setRequestsEntries ] = React.useState([""]);
    const [ p2nAuto, setP2nAuto ] = React.useState(true);

    const submit = React.useCallback(() => {
   
        const data = new FormData();
        //data.append("p2n_req", entry);// en cours de changement pour entry
        data.append("p2n_type", requestType)
        data.append("p2n_entries", requestsEntries.filter((r) => r).join(','))
        data.append("p2n_csv_file", selectedFile);
        data.append("p2n_csv_header", selectedHeader);
        data.append("p2n_dir", directory);
        data.append("p2n_options", options.join(','));
        data.append("p2n_auto", p2nAuto ? "true" : "false")
    
        console.log(data)
    
        fetch('http://localhost:5000/api/v1/requests', { 
          method: 'POST',
          body: data
        })
        .then(function(response) {
          return response.json();
        })
        .then(function(json) {
          if (json.code !== 400) {
            history.push("/app/requests/" + json.data.p2n_dir )
            window.location.reload(false);
          }

        });
    }, [directory, options, history, p2nAuto, requestType, requestsEntries, selectedFile, selectedHeader])

    
    const nextStep = React.useCallback((isLastStep) => {
        if (requestsEntries.some(requestsEntries => requestsEntries)) {
            setRequestsEntries(requestsEntries => requestsEntries.filter((r) => r))
        } else {
            setRequestsEntries([''])
        }

        if (!isLastStep) {
            setFocusID(focusID => focusID + 1);
        } else {
            submit()
        }

    }, [requestsEntries, submit])

    const upload = React.useCallback((file) => {
        setSelectedFile(file)

        if (file) {
            uploadFilesService.upload(file)
            .then((response) => {
                setCsvUploadInfo({
                    status: 'valide',
                    data: response.data
                })
                setSelectedHeader(response.data.headers[0])
            })
            .catch((error) => {
                setCsvUploadInfo({
                    status: 'error',
                    error: error
                })
                setSelectedHeader(null)
            });    
        }

    }, [])

    const verifyDirectoryAndSet = (directory) => {

        setDirectory(directory)

        fetch('http://localhost:5000/api/v1/directory/' + directory)
        .then((response) => response.json())
        .then((res) => {
            if(!res.exist) {
                setSafeDirectory(directory)
            }
        })
    }

    const selectFile = React.useCallback((file) => {
        upload(file)
    }, [upload])

    return (
        <div>
            <Step
                title="Choose the data source"
                id={0}
                focusID={focusID}
                setFocusID={setFocusID}
                nextStep={nextStep}
            >
                <ChooseRequestType
                    requestType={requestType}
                    setRequestType={setRequestType}
                />
            </Step>
            { requestType === 'request' ? (
                <Step 
                title="Request in CQL format"
                id={1}
                focusID={focusID}
                setFocusID={setFocusID}
                nextStep={nextStep}
                isValid={requestsEntries.some(e => e)}
                >
                    <RequestList
                        p2nAuto={p2nAuto}
                        setP2nAuto={setP2nAuto}
                        requestsEntries={requestsEntries}
                        setRequestsEntries={setRequestsEntries}
                    />
                </Step>
            ) : (
                <Step 
                title="CSV file"
                id={1}
                focusID={focusID}
                setFocusID={setFocusID}
                nextStep={nextStep}
                isValid={!!selectedFile}
                >
                <Upload
                    selectFile={selectFile}
                    selectedFile={selectedFile}
                    csvUploadInfo={csvUploadInfo}
                    selectedHeader={selectedHeader}
                    setSelectedHeader={setSelectedHeader}
                />
                </Step>
            )}
            <Step
                title="Request location"
                id={2}
                focusID={focusID}
                setFocusID={setFocusID}
                nextStep={nextStep}
                isValid={directory} 
            >
                <ChooseLocation
                    directory={directory}
                    safeDirectory={directory}
                    setDirectory={verifyDirectoryAndSet}
                />
            </Step>
            <Step
                title="Request options"
                id={3}
                focusID={focusID}
                setFocusID={setFocusID}
                nextStep={nextStep}
                isValid={directory} 
                isLastStep={true}
            >
                <ChooseOptions 
                    options={options}
                    setOptions={setOptions}
                />
            </Step>
        </div>
    )

}


export default Steps;