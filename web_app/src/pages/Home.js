
const Home = ({version}) => (
    <div className="container mx-auto">
        <div className="flex justify-center items-center">
            <div className="flex flex-col w-full lg:w-3/5 mb-12 bg-white p-8 rounded shadow">
                <h1 className="text-3xl font-semibold mb-2 text-gray-900">Patent2Net Docker Version : <span class="font-normal">{version}</span> </h1>
                <hr />
                <div className="mt-4">
                    <div className="mt-4">
                        <p className="text-gray-800 text-sm mb-4 text-justify">Patent2Net is a toolkit for patent information processing and statistical analysis for education and science.<br/>
                        Patent2Net helps to collect, study and analyze patent data from the European Patent Office’s Open Patent Services API (OPS). <br/>
                        Patent2Net is a free software dedicated to :
                        </p>	
                        
                        <ul className="list-disc text-gray-800 text-sm mb-3 text-justify">
                            <li>provide statistical analysis and representations of a set of patents.</li>
                            <li>promote the use of patent information in the academic field, nano and small firms,
                            developing countries.</li>
                            <li>study and practice how to collect, treat and communicate “textual bibliographic information”
                            and learn the automation process.</li>
                        </ul>
                        
                        <p className="text-gray-800 text-sm mb-4 text-justify">Contributions are always welcome!
                        </p>
                    </div>
                </div>
                <hr/>
                <div className="mt-4">
                    <p className="text-gray-800 text-sm mb-4 text-justify">To update your P2N version click on the button : </p>
                    <a href="/updateP2N"><input type="submit" name="Update P2N" value="Update P2N" className="w-64 focus:outline-none px-8 py-2 rounded-md font-semibold text-white bg-red-500 cursor-pointer mt-4" /></a>
                </div>
            </div>
        </div>
    </div>
)

export default Home