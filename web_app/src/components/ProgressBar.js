import React from "react"

const ProgressBar = ({ name, value, max_value }) => {

    const percent = React.useMemo(() => (value / max_value * 100) || 0, [value, max_value])
    const text = value === null || max_value === null ? "En attente..." : percent + "%"


    return (
        <div className="ProgressBar">
            <div className="flex justify-between">
                <p>{ name }</p>
                <p>{ text }</p>
            </div>
            <div className="relative pt-1">
                <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-orange-200">
                    <div style={{"width": percent + "%" }} className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-500"></div>
                </div>
            </div>
        </div>
    )
}

export default ProgressBar