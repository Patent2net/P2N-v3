import React, { useRef } from 'react';
import './index.css';

const Upload = ({ selectFile, selectedFile, csvUploadInfo, setSelectedHeader, selectedHeader }) => {
  
    const articleRef = useRef(null)
    const [counter, setCounter] = React.useState(0)
    const [draggedover, setDraggedover] = React.useState(false)
    const [selectHeaderOpen, setSelectHeaderOpen] = React.useState(false)
    

    // click the hidden input of type file if the visible button is clicked
    // and capture the selected files
    const onUploadButtonClick = React.useCallback(() => {
        document.getElementById("hidden-input").click();
    }, [])
    
    const onHiddenInputChange = React.useCallback((e) => {
        selectFile(e.target.files[0])
    }, [selectFile]);
    
    const hasFiles = ({ dataTransfer: { types = [] } }) =>
        types.indexOf("Files") > -1;

    const dropHandler = React.useCallback((ev) => {
        ev.preventDefault();

        selectFile(ev.dataTransfer.files[0]);
        setDraggedover(false)
        setCounter(0)

    }, [selectFile])
    
    const dragEnterHandler = React.useCallback((e) => {
        console.log("dragEnterHandler", e)
        e.preventDefault();
        if (!hasFiles(e)) {
        return;
        }
        setCounter(lastCounter => lastCounter + 1)
        setDraggedover(true)
    }, []);
    
    const dragLeaveHandler = React.useCallback((e) => {
        console.log("dragLeaveHandler", e)
        let newCounter = 0;
        setCounter(lastCounter => {
            newCounter = lastCounter - 1;
            return newCounter;
        })
        1 > newCounter && setDraggedover(false);
    }, []);
    
    const dragOverHandler = React.useCallback((e) => {
        console.log("dragOverHandler", e)
        if (hasFiles(e)) {
        e.preventDefault();
        }
    }, [])

    React.useEffect(() => {
        let article = articleRef.current
        article.addEventListener('dragenter', dragEnterHandler)
        article.addEventListener('dragleave', dragLeaveHandler)
        article.addEventListener('dragover', dragOverHandler)
        article.addEventListener('drop', dropHandler)
    }, [articleRef, dragEnterHandler, dragLeaveHandler, dragOverHandler, dropHandler])

    return (
        <article ref={articleRef} ariaLabel="File Upload Modal" className="relative h-full flex flex-col bg-white" >
            <div id="overlay" className={
                ((draggedover) ? "draggedover " : "") + "w-full h-full absolute top-0 left-0 pointer-events-none z-50 flex flex-col items-center justify-center rounded-md"
            }>
            <i>
                <svg className="fill-current w-12 h-12 mb-3 text-blue-700" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path d="M19.479 10.092c-.212-3.951-3.473-7.092-7.479-7.092-4.005 0-7.267 3.141-7.479 7.092-2.57.463-4.521 2.706-4.521 5.408 0 3.037 2.463 5.5 5.5 5.5h13c3.037 0 5.5-2.463 5.5-5.5 0-2.702-1.951-4.945-4.521-5.408zm-7.479-1.092l4 4h-3v4h-2v-4h-3l4-4z" />
                </svg>
            </i>
            <p className="text-lg text-blue-700">Drop file to upload</p>
            </div>

            

            <section className="h-full w-full h-full flex flex-col">
                <input id="hidden-input" type="file" className={"hidden"} onChange={onHiddenInputChange}/>
                { !selectedFile ? (
                    <header className="border-dashed border-2 border-gray-400 py-6 flex flex-col justify-center items-center">
                        <div className="w-full text-center flex flex-col items-center justify-center items-center">
                            <img className="mx-auto w-32" src="https://user-images.githubusercontent.com/507615/54591670-ac0a0180-4a65-11e9-846c-e55ffce0fe7b.png" alt="no data" />
                            <span className="text-small text-gray-500">No file selected</span>
                        </div>
                        <p className="mt-2 mb-3 font-semibold text-gray-900 flex flex-wrap justify-center">
                            <span>Drag and drop your</span>&nbsp;<span>file anywhere or</span>
                        </p>
                        <button id="button" className="rounded-sm px-3 py-1 bg-gray-200 hover:bg-gray-300 focus:shadow-outline focus:outline-none" onClick={onUploadButtonClick}>
                        Upload a file
                        </button>
                    </header>
                ) : (
                   
                    <article tabindex="0" class="group w-full h-full rounded-md focus:outline-none focus:shadow-outline elative bg-gray-100 cursor-pointer relative shadow-sm">
                        <div className="flex flex-row py-4 px-6 items-center">
                            <div class="flex flex-col break-words">
                                <h1 class="flex-1 group-hover:text-blue-800 text-base">{selectedFile.name}</h1>
                                <div class="flex">
                                    <span class="p-1 text-blue-800">
                                        <i>
                                        <svg class="fill-current w-4 h-4 ml-auto pt-1" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                                            <path d="M15 2v5h5v15h-16v-20h11zm1-2h-14v24h20v-18l-6-6z"></path>
                                        </svg>
                                        </i>
                                    </span>
                                    <p class="p-1 size text-xs text-gray-700">
                                        {
                                            selectedFile.size > 1024
                                            ? selectedFile.size > 1048576
                                            ? Math.round(selectedFile.size / 1048576) + "mb"
                                            : Math.round(selectedFile.size / 1024) + "kb"
                                            : selectedFile.size + "b"
                                        }
                                    </p>
                                </div>
                            </div>
                            <div class="ml-auto">
                                { csvUploadInfo && csvUploadInfo.status === 'valide' && csvUploadInfo.data.headers && (
                                    <div className="relative text-black w-36">
                                        <button type="button" className="relative w-full bg-white border border-gray-300 rounded-md shadow-sm pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 font-semibold" aria-haspopup="listbox" aria-expanded="true" aria-labelledby="listbox-label" onClick={() => setSelectHeaderOpen(!selectHeaderOpen)}>
                                            <span className="flex items-center">
                                                <span className="ml-3 block truncate">{ selectedHeader }</span>
                                            </span>
                                            <span className="ml-3 absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                                                <svg className="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                                <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                                                </svg>
                                            </span>
                                        </button>

                                        <ul style={{maxHeight: 200}} className={"absolute z-10 mt-2 w-full bg-white shadow-lg rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm" + (!selectHeaderOpen ? " transition ease-in duration-100 opacity-0" : " opacity-100")} tabindex="-1" role="listbox" aria-labelledby="listbox-label" aria-activedescendant="listbox-option-3">
                                        
                                            { csvUploadInfo.data.headers.map((header) => (
                                                <li className="text-gray-900 cursor-default select-none relative py-2 pl-3 pr-9" id="listbox-option-0" role="option" onClick={() => {
                                                    setSelectedHeader(header);
                                                    setSelectHeaderOpen(false);
                                                }}>
                                                    <div className="flex items-center">
                                                
                                                        <span className="font-normal ml-3 block truncate">
                                                            { header }
                                                        </span>
                                                    </div>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )} 
                            </div>
                            <button class="delete focus:outline-none hover:bg-gray-300 p-3 rounded-md text-gray-800" data-target="blob:https://tailwindcomponents.com/479642a1-81dd-47f1-8300-a8d5983a5c5d" onClick={() => selectFile(undefined)}>
                                <svg class="pointer-events-none fill-current w-4 h-4 ml-auto" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                                <path class="pointer-events-none" d="M3 6l3 18h12l3-18h-18zm19-4v2h-20v-2h5.711c.9 0 1.631-1.099 1.631-2h5.316c0 .901.73 2 1.631 2h5.711z"></path>
                                </svg>
                            </button>
                        </div>
                    </article>

                )}
            </section>
        </article>
    )
}

export default Upload;