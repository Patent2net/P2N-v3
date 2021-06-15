
const GetStarted = () => {
    
    return (
        <div className="container mx-auto">
            <div className="flex justify-center items-center">
                <div className="flex flex-col w-full lg:w-3/5 mb-12 bg-white p-8 rounded shadow">
                    <div>
                        <h1 className="text-4xl font-semibold mb-2 text-gray-900">Get Started</h1>
                        <hr/>
                        
                        <div className="mt-4">

                            <h2 className="text-lg mb-2 font-bold" id="Register" >Register the use of P2N</h2>
                            <hr/>

                            <div className="mt-4">
                                <p className="text-gray-800 text-sm mb-4 text-justify">You have first to register yourself at Espacenet and get a key to data access. So you must (if you already have it skip this step)
                                </p>	
                                
                                <ol className="list-decimal text-gray-800 text-sm mb-3 text-justify">
                                    <li>Go to the Open Patent Services (OPS) by opening the link :<br/> 
                                    <a className="hover:underline" href="https://www.epo.org/searching-for-patents/technical/espacenet/ops.html#tab1"> https://www.epo.org/searching-for-patents/technical/espacenet/ops.html#tab1</a></li>
                                    <li>Click on the “<b>Register</b>” button and fulfill the form</li>
                                    <li>Wait until you receive the email confirmation of you register from EPO Developer Portal.</li>
                                    <li>Log in the EPO Developer Portal :<br /> <a className="hover:underline" href=" https://developers.epo.org/user/login">https://developers.epo.org/user/login</a> </li>
                                    <li>Select the option “<b>My apps</b>”</li>
                                    <li>Create and register the “<b>Patent2Net</b>” application</li>
                                    <li> The system returns the API credentials key and secret, similar to that shown bellow (this one is invalid, of course):<br/>
                                    <pre className="code border-dashed border-2 border-orange-600 bg-orange-100">vmrr7AaAGIl794E6VunJ6PzjbkfajwLW,KHzH4fGM7opMhDDD</pre>
                                    </li>
                                    <li>Copy/paste the key in the textbox and click on confirm. It will create a file in your install of Patent2Net who will let you have full use of it. </li>
                                </ol>
                                
                            </div>
                        </div>
                        <div className="mt-4">
                            <form action="http://localhost:5000/get_started/stocked" method="post">
                                <div>
                                    <label className="font-semibold">cles-epo * :</label>
                                    <p className="pt-2 pb-2 text-sm italic text-gray-800">Paste in the textbox the key provided by EPO.</p>
                                </div>
                                <div className="mb-2">
                                    <input className="px-3 py-4 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-base border border-blueGray-300 outline-none focus:outline-none focus:ring w-full" type="text" required placeholder="vmrr7AaAGIl794E6VunJ6PzjbkfajwLW,KHzH4fGM7opMhDDD" name="p2n_epo" />
                                </div>

                            
                                <div className="mt-4 italic text-sm text-gray-800">
                                    Fields marked with * are mandatory.
                                </div>
                                <input className="w-64 focus:outline-none px-8 py-2 rounded-md font-semibold text-white bg-indigo-500 cursor-pointer mt-4" type="submit" value="confirm" id="pacing"/>
                            </form>
                        </div>
                    </div>
                    <div className="mt-4">
                        <h2 className="text-lg mb-2 font-bold"Id="Archive_Content" >P2N Docker archive content</h2>
                        <hr/>
                    </div>
                    <div className="mt-2">
                        <div>
                            <ul className="list-disc text-gray-800 text-sm mb-3 mt-3 text-justify ">
                                <li> <b>Dockerfile</b> : Mandatory for the install of P2N Docker</li>
                                <li><b>Install_P2N.bat</b> : used to install all the P2N Content in Docker</li>
                                <li><b>Run_P2N.bat</b> : Used to initiate P2N instance in Docker</li>
                                <li><b>Stop_P2N.bat</b> : Used to stop P2N instance</li>
                                <li><b>Copy Docker P2N</b> :
                                    <ul>
                                        <li>Copy_Docker_P2N.bat : Create a tar file with all the base content of your docker version</li>
                                        <li>Load_Docker_P2N.bat : Import the tar file insde docker and create P2N image</li>
                                    </ul>
                                </li>
                                <li><b>P2N_Bash.bat</b> : Create a command prompt instance who interact with P2N Docker. <a href="https://docs.ip-tools.org/patent2net/usage/classic.html"target="_blank" className="hover:underline"><i>Click here for more details.</i></a></li>
                            </ul>
                        </div>
                    </div>
                    <div className="mt-4">
                        <h2 className="text-lg mb-2 font-bold" Id="Interface_Directory">P2N Interface directories</h2>
                        <hr/>
                    </div>
                    <div className="mt-2">
                        <div>
                            <ul className="list-disc text-gray-800 text-sm mb-3 mt-3 text-justify ">
                                <li> <b> Home</b> : Default page. Explain how PatentNet can help you</li>
                                <li><b>Get Started</b> : Explain how to use P2N Docker</li>
                                <li><b>Requests</b> : form used to execute requests to the EPO database </li>
                                <li><b>Index</b> : Display all the results of P2N </li>
                                <li><b>Download Data</b> : create a zip folder with all the datas contained in Index. Downloaded on your local machine</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default GetStarted;