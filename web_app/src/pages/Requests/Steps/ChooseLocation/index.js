import React from 'react';

const ChooseLocation = ({ directory, setDirectory }) => {

    return (
        <div className="grid grid-cols-12">
          <div className="col-start-1 col-span-7">
            <p className="pb-2 text-sm text-gray-800">Enter in the textbox where your patent research will be stocked.</p>
            <input 
              value={directory} 
              onChange={(e) => setDirectory(e.target.value)}
              className="focus:shadow-outline px-3 py-4 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-base border border-blueGray-300 outline-none focus:outline-none focus:ring w-full" 
              type="text" 
              required 
              placeholder="Exemple: lentille" 
              name="p2n_dir" pattern="[A-Za-z0-9_-]{1,}" 
              title="Use only lowercase [a-z], Uppercase [A-Z], Numbers[0-9], Underscore[_] and Hyphen [-]" 
            />
          </div>
        </div>
    )

}

export default ChooseLocation;