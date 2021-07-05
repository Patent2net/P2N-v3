import React from 'react'
import UploadService from '../../services/upload-files.service'
import Upload from './Upload/index'

const CSVUpload = () => {

    const [csvUploadInfo, setCsvUploadInfo] = React.useState();
    const [selectedFile, setSelectedFile] = React.useState();
    const [selectedHeader, setSelectedHeader] = React.useState();

    const upload = React.useCallback((file) => {
        setSelectedFile(file)

        if (file) {
            UploadService.upload(file)
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

    const selectFile = React.useCallback((file) => {
        upload(file)
    }, [upload])

    return (
        // <div>
        //     <label className="btn btn-default">
        //         <input type="file" onChange={selectFile} />
        //     </label>

        //     <button 
        //         className="btn btn-success"
        //         disabled={!selectedFiles}
        //         onClick={upload}
        //     >
        //         Upload
        //     </button>

        //     <div className="alert alert-light" role="alert">
        //         {message}
        //     </div>

        //     <div className="card">
        //         <div className="card-header">List of Files</div>
        //         <ul className="list-group list-group-flush">
        //             { fileInfos && fileInfos.map((file, index) => (
        //                 <li className="list-group-item" key={index}>
        //                     {file}
        //                 </li>
        //             ))}
        //         </ul>
        //     </div>
        // </div>
        <>
            <div className="mt-4 pb-4">
                <label className="text-lg mb-2 font-bold">Import CSV file</label>
            </div>
            <Upload 
                selectFile={selectFile}
                selectedFile={selectedFile}
                csvUploadInfo={csvUploadInfo}
                selectedHeader={selectedHeader}
                setSelectedHeader={setSelectedHeader}
            />
        </>
    )
}


export default CSVUpload;