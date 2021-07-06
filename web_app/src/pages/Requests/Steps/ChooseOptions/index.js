import classNames from 'classnames';
import React from 'react';

const ChooseOptions = ({ options, setOptions }) => {

    const toggleCheckbox = React.useCallback((key) => {
        setOptions((options) => !options.includes(key) ? [...options, key] : [...options.filter((value) => value !== key)] )
    }, [setOptions])

      
    return (
        <div>
            <p className="pb-4 text-sm text-gray-800">Click on the checkbox to specify the elements you need in your research</p>
            <div className="grid grid-cols-2 gap-3">
                {Object.keys(all_options).map((key, index) => {
                    let option = all_options[key]
                    return (
                    <div 
                        className={
                            classNames(
                                "cursor-pointer box-border flex flex-col text-left border-2 text-sm", 
                                options.includes(key) ? "rounded p-3 border-indigo-600 text-indigo-600" : "rounded p-3 opacity-30 opacity-50"
                            )
                        }
                        onClick={() => toggleCheckbox(key)}
                    >
                        <p className="font-medium text-indigo-600">{option["name"]}</p>
                        <p className="inline text-gray-800">{option["description"]}</p>
                    </div>
                    )
                })}
            </div>
        </div>
    )

}

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

export default ChooseOptions;