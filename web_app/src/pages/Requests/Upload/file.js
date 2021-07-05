import React from 'react';

const UploadFile = ({ title }) => {

    return (
        <li className="block p-1 w-1/2 sm:w-1/3 md:w-1/4 lg:w-1/6 xl:w-1/8 h-24">
            <article tabindex="0" className="group w-full h-full rounded-md focus:outline-none focus:shadow-outline elative bg-gray-100 cursor-pointer relative shadow-sm">
            <img alt="upload preview" className="img-preview hidden w-full h-full sticky object-cover rounded-md bg-fixed" />

            <section className="flex flex-col rounded-md text-xs break-words w-full h-full z-20 absolute top-0 py-2 px-3">
                <h1 className="flex-1 group-hover:text-blue-800">{title}</h1>
                <div className="flex">
                <span className="p-1 text-blue-800">
                    <i>
                    <svg className="fill-current w-4 h-4 ml-auto pt-1" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                        <path d="M15 2v5h5v15h-16v-20h11zm1-2h-14v24h20v-18l-6-6z" />
                    </svg>
                    </i>
                </span>
                <p className="p-1 size text-xs text-gray-700"></p>
                <button className="delete ml-auto focus:outline-none hover:bg-gray-300 p-1 rounded-md text-gray-800">
                    <svg className="pointer-events-none fill-current w-4 h-4 ml-auto" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                    <path className="pointer-events-none" d="M3 6l3 18h12l3-18h-18zm19-4v2h-20v-2h5.711c.9 0 1.631-1.099 1.631-2h5.316c0 .901.73 2 1.631 2h5.711z" />
                    </svg>
                </button>
                </div>
            </section>
            </article>
        </li>
    )
}

export default UploadFile;