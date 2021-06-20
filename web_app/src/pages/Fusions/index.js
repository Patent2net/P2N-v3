import React from "react";
import { useHistory } from "react-router";
import { Link } from "react-router-dom";


function Fusions() {

  const [ data, setData ] = React.useState({});

  React.useEffect(() => {
      fetch("http://localhost:5000/api/v1/fusions")
      .then(function(response) {
          return response.json();
      })
      .then(function(json) {
        if (json.data) {
          setData(json.data)
        }
        console.log(json.data)
      });
  }, []);
    
  return (
    <div className="container mx-auto grid grid-cols-4 gap-4 items-start">
      <div className="col-start-1 bg-white p-8 rounded shadow">
        
        <div className="mb-6 flex flex-col">
          <h3 className="text-lg mb-2 font-bold">Fusions terminés</h3>

          { data.fusions && data.fusions.filter(fusion => fusion.done).map((fusion) => (
            <Link to={"/app/requests/" + fusion.content.main } key={fusion.content.main}>{fusion.content.main}</Link>
          ))}

          { !data.fusions && (
            <div className="grid grid-cols-1 gap-2">
              <span className="skeleton-box h-5 w-3/5 inline-block"></span>
              <span className="skeleton-box h-5 w-1/2 inline-block"></span>
              <span className="skeleton-box h-5 w-2/5 inline-block"></span>
            </div>
          ) }
        </div>
        
        <hr class="mb-3"/>

        <div class="mb-6 flex flex-col">
          <h3 className="text-lg mb-2 font-bold">Fusions en cours</h3>
          <div className="">
            <div className="relative pt-1">
              { data.fusions && data.fusions.filter(fusion => fusion.in_progress).map((fusion) => (
                <Link to={"/app/requests/" + fusion.content.main} key={fusion.content.main}>
                  <p class="mb-1">{ fusion.content.main }</p>

                </Link>
              ))}

              { !data.fusions && (
                  <div className="grid grid-cols-1 gap-2">
                    <span className="skeleton-box h-5 w-3/5 inline-block"></span>
                    <span className="skeleton-box h-5 w-1/2 inline-block"></span>
                    <span className="skeleton-box h-5 w-2/5 inline-block"></span>
                  </div>
                ) }
            </div>
          </div>
        </div>

        <hr class="mb-3"/>


        <div className="mb-6 flex flex-col">
          <h3 className="text-lg mb-2 font-bold">Fusions en attente</h3>

          { data.fusions && data.fusions.filter(fusion => !fusion.in_progress && !fusion.done).map((fusion) => (
            <Link to={"/app/requests/" + fusion.content.main } key={fusion.content.main}>{fusion.content.main}</Link>
          ))}

          { !data.fusions && (
            <div className="grid grid-cols-1 gap-2">
              <span className="skeleton-box h-5 w-3/5 inline-block"></span>
              <span className="skeleton-box h-5 w-1/2 inline-block"></span>
              <span className="skeleton-box h-5 w-2/5 inline-block"></span>
            </div>
          ) }
        </div>
      </div>
    </div>
  );
}

export default Fusions;
