import React from "react";
import { useHistory } from "react-router";
import { Link } from "react-router-dom";
import Entries from './Entries/index'
import Icon from "../icon";
import Steps from "./Steps";

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

function Requests() {

  const [ requests, setRequests ] = React.useState({});

  React.useEffect(() => {
      fetch("http://localhost:5000/api/v1/requests")
      .then((response) => response.json())
      .then(function(json) {
        if (json.data) {
          setRequests(json.data)
        }
      });
  }, []);

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
        
        <hr className="mb-3"/>

        <div className="mb-6 flex flex-col">
          <h3 className="text-lg mb-2 font-bold">Requêtes en cours</h3>
          <div className="">
            <div className="relative pt-1">
              { requests.in_progress && requests.in_progress.map((name) => (
                <Link to={"/app/requests/" + name} key={name}>
                  <p className="mb-1">{ name }</p>
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
        </div>
        <Steps />
      </div>
    </div>
  );
}

export default Requests;
