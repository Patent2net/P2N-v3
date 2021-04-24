
function App() {
  return (
    <div className="bg-orange-100 flex justify-between">
      <div className=" flex flex-col mt-12 mb-12 bg-white p-8 rounded shadow ">
        <h3 className="mb-2">Previous request(s)</h3>
      </div>
        
      <div className="flex flex-col mt-12 mb-12 bg-white p-8 rounded shadow ">
        <h1 className="text-lg mb-2 text-gray-900">Patent2Net toolkit</h1>
        <div className="mt-4">

          <form action="/requests" method="post">
            <div>
              <label className="font-semibold">Request in CQL format * :</label>
              <p className="pt-2 pb-2 text-sm italic text-gray-800">Enter in the textbox a valid espacenet smart search query for your patent research.</p>
            </div>
            <div className="mb-2">
              <input className="text-sm border px-2 py-1 rounded w-full" type="text" required placeholder="TA=lentille" name="p2n_req" id="p2n_reqBtn" />
            </div>

            <div>
              <label className="font-semibold">Request Location * :</label>
              <p className="pt-2 pb-2 text-sm italic text-gray-800">Enter in the textbox where your patent research will be stocked.</p>
            </div>
            <div className="mb-2">
              <input className="text-sm border px-2 py-1 rounded w-full" type="text" required placeholder="lentille" name="p2n_dir" pattern="[A-Za-z0-9_-]{1,}" title="Use only lowercase [a-z], Uppercase [A-Z], Numbers[0-9], Underscore[_] and Hyphen [-]" />
            </div>				

            <div className="mt-4">
            <label className="font-semibold">Request Options :</label>
              <p className="pt-2 pb-2 text-sm italic text-gray-800">Click on the checkbox to specify the elements you need in your research:</p>
              <p>
                <input type="checkbox" id="p2n_family" name="p2n_family" value="True" checked />
                <input type="hidden" name="p2n_family" value="False" /> 
                <label for="p2n_family" className="text-gray-800 text-sm mb-4 text-justify"><b>p2n family</b>: run family data acquisition </label>
                <input type="hidden" name="p2n_content" value="True" />
                <input type="hidden" name="p2n_gather_biblio" value="True" />
              </p>

              <p>
                <input type="checkbox" id="p2n_image" name="p2n_image" value="True" checked />
                <input type="hidden" name="p2n_image" value="False" /> 
                <label for="p2n_images" className="text-gray-800 text-sm mb-4 text-justify"><b>p2n images</b>: Fetch images</label>
              </p>

              <p>
                <input type="checkbox" id="p2n_network" name="p2n_network" value="True" checked />
                <input type="hidden" name="p2n_network" value="False" /> 
                <label for="p2n_networks" className="text-gray-800 text-sm mb-4 text-justify"><b>p2n networks</b>: Build various artefacts for data exploration based on network graphs</label>
              </p>

              <p>
                <input type="checkbox" id="p2n_freeplane" name="p2n_freeplane" value="True" checked />
                <input type="hidden" name="p2n_freeplane" value="False" /> 
                <label for="p2n_freeplane" className="text-gray-800 text-sm mb-4 text-justify"><b>p2n freeplane</b>: Build mind map for Freeplane</label>
              </p>

              <p>
                <input type="checkbox" id="p2n_bibfile" name="p2n_bibfile" value="True" checked />
                <input type="hidden" name="p2n_bibfile" value="False" /> 
                <label for="p2n_bibfiles" className="text-gray-800 text-sm mb-4 text-justify"><b>p2n bibfile</b>: Export data in bibfile format</label>
              </p>
              
              <p>
                <input type="checkbox" id="p2n_map" name="p2n_map" id="p2n_mapBtn" value="True" checked />
                <input type="hidden" name="p2n_map" value="False" /> 
                <label for="p2n_maps" className="text-gray-800 text-sm mb-4 text-justify"><b>p2n maps</b>: Build maps of country coverage of patents, as well as applicants and inventors </label>
              </p>
              
              <p>
                <input type="checkbox" id="p2n_tables" name="p2n_tables" value="True" checked />
                <input type="hidden" name="p2n_tables" value="False" /> 
                <label for="p2n_tables" className="text-gray-800 text-sm mb-4 text-justify"><b>p2n tables</b>: Export various artefacts for tabular data exploration</label>
              </p>

              <p>
                <input type="checkbox" id="p2n_carrot" name="p2n_carrot" value="True" checked />
                <input type="hidden" name="p2n_carrot" value="False" />
                <label for="p2n_carrot" className="text-gray-800 text-sm mb-4 text-justify"><b>p2n carrot</b>: Export data to XML suitable for using in Carrot</label>
              </p>				
              
              <p>
                <input type="checkbox" id="p2n_iramuteq" name="p2n_iramuteq" value="True" checked />
                <input type="hidden" name="p2n_iramuteq" value="False" /> 
                <label for="p2n_iramuteq" className="text-gray-800 text-sm mb-4 text-justify"><b>p2n iramuteq </b>: Fetch more data and export it to suitable format for using in Iramuteq</label>
              </p>

              <p>
                <input type="checkbox" id="p2n_cluster" name="p2n_cluster" value="True" checked />
                <input type="hidden" name="p2n_cluster" value="False" /> 
                <label for="p2n_cluster" className="text-gray-800 text-sm mb-4 text-justify"><b>p2n cluster </b>: Double clustering system based on non so trivial words</label>
              </p>
            </div>
            <input className="bg-orange-600 hover:bg-orange-700 cursor-pointer px-2 py-1 text-white rounded mt-4" type="submit" value="Submit" id="pacing"/>
            <div className="mt-4 italic text-sm text-gray-800">
              Fields marked with * are mandatory.
            </div>
          </form>
        </div>
      </div>
      <div className=" flex flex-col mt-12 mb-12 bg-white p-8 rounded shadow ">
        <h3 className="mb-2">Requetes en cours</h3>
        <div className="ProgressElement">
          <div className="ProgressElement__infos">
            
          </div>
          <div className="relative pt-1">
            <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-orange-200">
              <div style={{"width": "30%"}} className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-orange-500"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
