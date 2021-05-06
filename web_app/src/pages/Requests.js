import React from "react";
import { useHistory } from "react-router";
import { Link } from "react-router-dom";

const all_options = {
  "p2n_family": {
    name: "p2n family",
    description: "run family data acquisition"
  },
  "p2n_image": {
    name: "p2n images",
    description: "Fetch images"
  },
  "p2n_network": {
    name: "p2n networks",
    description: "Build various artefacts for data exploration based on network graphs"
  },
  "p2n_freeplane": {
    name: "p2n freeplane",
    description: "Build mind map for Freeplane"
  },
  "p2n_bibfile": {
    name: "p2n bibfile",
    description: "Export data in bibfile format"
  },
  "p2n_map": {
    name: "p2n maps",
    description: "Build maps of country coverage of patents, as well as applicants and inventors"
  },
  "p2n_tables": {
    name: "p2n tables",
    description: "Export various artefacts for tabular data exploration"
  },
  "p2n_carrot": {
    name: "p2n carrot",
    description: "Export data to XML suitable for using in Carro"
  },
  "p2n_iramuteq": {
    name: "p2n iramuteq",
    description: "Fetch more data and export it to suitable format for using in Iramuteq"
  },
  "p2n_cluster": {
    name: "p2n cluster",
    description: "Double clustering system based on non so trivial words"
  },
}

function App() {

  const [ request, setRequest ] = React.useState("");
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

  const onSubmit = React.useCallback((event) => {
    event.preventDefault()

    const data = new FormData();
    data.append("p2n_req", request);
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
      history.push("/app/requests/" + json.data.p2n_dir );
    });
    

  }, [request, directory, options, history, p2nAuto])

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
        <h1 className="text-3xl font-semibold mb-2 text-gray-900">Patent2Net toolkit</h1>
        <hr />
        <div className="mt-4">

          <form onSubmit={onSubmit}>
            <div>
              <label className="font-semibold">Request in CQL format * :</label>
              <p className="pt-2 pb-2 text-sm italic text-gray-800">Enter in the textbox a valid espacenet smart search query for your patent research.</p>
            </div>
            <div className="mb-2">
              <input
                value={request} 
                onChange={(e) => setRequest(e.target.value)}
                className="px-3 py-4 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-base border border-blueGray-300 outline-none focus:outline-none focus:ring w-full"
                type="text"
                required
                placeholder="TA=lentille"
                name="p2n_req"
                id="p2n_reqBtn"
              />
            </div>

            <div>
              <label className="font-semibold">Request Location * :</label>
              <p className="pt-2 pb-2 text-sm italic text-gray-800">Enter in the textbox where your patent research will be stocked.</p>
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
            <label className="font-semibold">Request Options :</label>
              <p className="pt-2 pb-2 text-sm italic text-gray-800">Click on the checkbox to specify the elements you need in your research:</p>
              
              {Object.keys(all_options).map((key, index) => {
                let option = all_options[key]
                return (
                  <p key={key}>
                    <input 
                      type="checkbox"
                      id={key}
                      name={key} 
                      checked={options.includes(key)} 
                      onChange={() => toggleCheckbox(key) }
                    />
                    <label htmlFor={key} className="text-gray-800 text-sm mb-4 text-justify"><b>{ option["name"] }</b>: { option["description"] } </label>
                  </p>
                )
              })}
            </div>
            <div className="mt-4">
              <label className="font-semibold">Use auto request splitter:</label>
              <input 
                type="checkbox"
                name={"p2n_auto"} 
                checked={p2nAuto} 
                onChange={() => setP2nAuto(!p2nAuto) }
              />
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

export default App;
