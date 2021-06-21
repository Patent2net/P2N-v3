import React from "react";
import { useHistory } from "react-router";
import { Link } from "react-router-dom";
import Entries from './Entries/index'
import Icon from "../icon";

const all_options = {
  "p2n_family": {
    name: "p2n family",
    description: "run family data acquisition",
    icon: "family"
  },
  "p2n_image": {
    name: "p2n images",
    description: "Fetch images",
    icon: "image"
  },
  "p2n_network": {
    name: "p2n networks",
    description: "Build various artefacts for data exploration based on network graphs",
    icon: "network"
  },
  "p2n_freeplane": {
    name: "p2n freeplane",
    description: "Build mind map for Freeplane",
    icon: "nodes"
  },
  "p2n_bibfile": {
    name: "p2n bibfile",
    description: "Export data in bibfile format",
    icon: "archive"
  },
  "p2n_map": {
    name: "p2n maps",
    description: "Build maps of country coverage of patents, as well as applicants and inventors",
    icon: "map"
  },
  "p2n_tables": {
    name: "p2n tables",
    description: "Export various artefacts for tabular data exploration",
    icon: "table"
  },
  "p2n_carrot": {
    name: "p2n carrot",
    description: "Export data to XML suitable for using in Carro",
    icon: "carrot"
  },
  "p2n_iramuteq": {
    name: "p2n iramuteq",
    description: "Fetch more data and export it to suitable format for using in Iramuteq",
    icon: "chart-pie"
  },
  "p2n_cluster": {
    name: "p2n cluster",
    description: "Double clustering system based on non so trivial words",
    icon: "cluster"
  },
}

const entryTypes = {
  REQUEST: 'REQUEST',
  REQUESTS: 'REQUESTS',
  CSV: 'CSV'
}

function Requests() {

  const [ entryType, setEntryType ] = React.useState(entryTypes.REQUEST);

  const [ requestEntry, setRequestEntry ] = React.useState("");
  const [ requestsEntry, setRequestsEntry ] = React.useState([""]);

  const [ directory, setDirectory ] = React.useState("");
  const [ options, setOptions ] = React.useState([
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
  const [ requests, setRequests ] = React.useState({});
  const [ p2nAuto, setP2nAuto ] = React.useState(false);

  const history = useHistory();

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

  const toggleCheckbox = React.useCallback((key) => {
    setOptions((options) => !options.includes(key) ? [...options, key] : [...options.filter((value) => value !== key)] )
  }, [setOptions])

  
  const getCurrentEnry = React.useCallback(() => {
      if (entryType === entryTypes.REQUEST) return requestEntry
      if (entryType === entryTypes.REQUESTS) return requestsEntry.filter((r) => r).join(',')
      return null
    }, [entryType, requestEntry, requestsEntry]
  )
  const onSubmit = React.useCallback((event) => {
    event.preventDefault()

    const data = new FormData();
    //data.append("p2n_req", entry);// en cours de changement pour entry
    data.append("p2n_entrytype", entryType)
    data.append("p2n_entry", getCurrentEnry())
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
      console.log(json)
      if (entryType === entryTypes.REQUEST) history.push("/app/requests/" + json.data.p2n_dir );

      window.location.reload(false);
    });
  }, [directory, options, history, p2nAuto, entryType, getCurrentEnry])


  return (
    <div className="container mx-auto grid grid-cols-4 gap-4 items-start">
      <div className="col-start-1 bg-white p-8 rounded shadow">
        
        <div className="mb-6 flex flex-col">
          <h3 className="text-lg mb-2 font-bold">Requêtes précédentes</h3>

          { requests.done && requests.done.map((name) => (
            <Link to={"/app/requests/" + name } key={name}>{name}</Link>
          ))}

          { !requests.done && (
            <div className="grid grid-cols-1 gap-2">
              <span className="skeleton-box h-5 w-3/5 inline-block"></span>
              <span className="skeleton-box h-5 w-1/2 inline-block"></span>
              <span className="skeleton-box h-5 w-2/5 inline-block"></span>
            </div>
          ) }
        </div>
        
        <hr class="mb-3"/>

        <div class="mb-6 flex flex-col">
          <h3 className="text-lg mb-2 font-bold">Requêtes en cours</h3>
          <div className="">
            <div className="relative pt-1">
              { requests.in_progress && requests.in_progress.map((name) => (
                <Link to={"/app/requests/" + name} key={name}>
                  <p class="mb-1">{ name }</p>
                  {
                    requests.global_progress && requests.global_progress[name] && (
                      <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-orange-200">
                        <div 
                          style={{"width": (requests.global_progress[name].done_step_count / requests.global_progress[name].total_step_count * 100) + "%"}} 
                          className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-500"
                        ></div>
                        <div 
                          style={{"width": (requests.global_progress[name].progress_step_count / requests.global_progress[name].total_step_count * 100) + "%"}} 
                          className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-orange-300"
                        ></div>
                      </div>
                    )
                  }
                </Link>
              ))}

              { !requests.in_progress && (
                  <div className="grid grid-cols-1 gap-2">
                    <span className="skeleton-box h-5 w-3/5 inline-block"></span>
                    <span className="skeleton-box h-5 w-1/2 inline-block"></span>
                    <span className="skeleton-box h-5 w-2/5 inline-block"></span>
                  </div>
                ) }
            </div>
          </div>
        </div>
      </div>
        
      <div className="col-span-3 flex flex-col mb-12 bg-white p-8 rounded shadow ">
        <div className="flex justify-between items-center pb-2 flex-wrap">
          <h1 className="text-4xl font-semibold mb-2 text-gray-900">Patent2Net toolkit</h1>      
          <div className='border-bottom flex'>
            <ul className='flex cursor-pointer bg-gray-200 rounded-lg'>
                <li onClick={() => setEntryType(entryTypes.REQUEST)} className={'py-2 px-6 rounded-lg' + ((entryType === entryTypes.REQUEST) ? ' bg-indigo-600 text-white' : ' text-gray-500 bg-gray-200')}>One request</li>
                <li onClick={() => setEntryType(entryTypes.REQUESTS)} className={'py-2 px-6 rounded-lg' + ((entryType === entryTypes.REQUESTS) ? ' bg-indigo-600 text-white' : ' text-gray-500 bg-gray-200')}>Multiple request</li>
                <li onClick={() => setEntryType(entryTypes.CSV)} className={'py-2 px-6 rounded-lg' + ((entryType === entryTypes.CSV) ? ' bg-indigo-600 text-white' : ' text-gray-500 bg-gray-200')}>CSV</li>
            </ul>
          </div>
        </div>
       
        <hr />
        <div className="mt-4">

          <form onSubmit={onSubmit}>

            <Entries 
              entryType={entryType}
              entries={{
                requestEntry,
                requestsEntry,
                setRequestEntry,
                setRequestsEntry
              }}
            ></Entries>

            <div class="mt-4">
              <label className="text-lg mb-2 font-bold">Request Location</label>
              <p className="pb-2 text-sm italic text-gray-800">Enter in the textbox where your patent research will be stocked.</p>
            </div>
            <div className="mb-2">
              <input 
                value={directory} 
                onChange={(e) => setDirectory(e.target.value)}
                className="px-3 py-4 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-base border border-blueGray-300 outline-none focus:outline-none focus:ring w-full" 
                type="text" 
                required 
                placeholder="lentille" 
                name="p2n_dir" pattern="[A-Za-z0-9_-]{1,}" 
                title="Use only lowercase [a-z], Uppercase [A-Z], Numbers[0-9], Underscore[_] and Hyphen [-]" 
              />
            </div>				

            <div className="mt-4">
            <label className="text-lg mb-2 font-bold">Request Options</label>
              <p className="pb-2 text-sm italic text-gray-800">Click on the checkbox to specify the elements you need in your research:</p>
              
              <div className="grid grid-flow-row grid-cols-3 gap-2">
                {Object.keys(all_options).map((key, index) => {
                  let option = all_options[key]
                  return (
                    <div 
                      class={
                        options.includes(key) ? 
                          "cursor-pointer box-border flex flex-col justify-center items-center rounded p-3 text-center border-2 border-indigo-600 text-indigo-600" :
                          "cursor-pointer box-border flex flex-col justify-center items-center border rounded p-3 text-center opacity-30"
                      }
                      onClick={() => toggleCheckbox(key)}
                    >
                      <div className="icon text-black">
                        <Icon name={option.icon} />
                      </div>
                      <p class="text-sm font-semibold pt-2">{option["name"]}</p>
                      <p class="text-xs pt-1">{option["description"]}</p>
                    </div>
                  )
                })}
              </div>
            </div>
            <div className="mt-4">
              <label className="text-lg mb-2 font-bold">Request splitter</label>
              <div class="w-1/2 pt-2">
                <div 
                  class={
                    p2nAuto ? 
                      "cursor-pointer box-border flex flex-col justify-center items-center rounded p-3 text-center border-2 border-indigo-600 text-indigo-600" :
                      "cursor-pointer box-border flex flex-col justify-center items-center border rounded p-3 text-center opacity-30"
                  }
                  onClick={() => setP2nAuto(!p2nAuto)}
                >
                  <div className="icon text-black">
                    <Icon name="split" />
                  </div>
                  <p class="text-sm font-semibold pt-2">Use auto request spliter</p>
                  <p class="text-xs pt-1">
                    It allows to exceed the limit of 2000 patents per request by splitting it into several sub-request
                  </p>
                </div>
              </div>
            </div>
            <div className="mt-4 italic text-sm text-gray-800">
              Fields marked with * are mandatory.
            </div>
            <input 
              className="w-64 focus:outline-none px-8 py-2 rounded-md font-semibold text-white bg-indigo-500 cursor-pointer mt-4"
              type="submit"
              value="Submit"
            />
          </form>
        </div>
      </div>
    </div>
  );
}

export default Requests;
