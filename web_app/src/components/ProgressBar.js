import React from "react"

const ProgressBar = ({ name, value, max_value }) => {

    const percent = React.useMemo(() => (value / max_value * 100) || 0, [value, max_value])
    const text = value === null || max_value === null ? "En attente..." : percent + "%"
var corresp = {
    p2n_req: "Gathering patent list",
    p2n_filtering: "Filtering",
	p2n_gather_biblio: "Gathering metadata",
	p2n_content: "Gathering content",
	p2n_family: "Gathering families",
	p2n_image: "Gathering and processing images",
	p2n_network: "Processing networks",
	p2n_tables: "Processing tables",
	p2n_carrot: "Preparing for carrot",
	p2n_iramuteq: "Preparing for Iramuteq",
	p2n_cluster: "Clustering",
	p2n_map: "Processing cartographies",
    p2n_indexer: "Indexing"
};


    return (
        <div class="ProgressBar">
            <div class="flex justify-between">
                <p>{ corresp[name] }</p>
                <p>{ text }</p>
            </div>
            <div class="relative pt-1">
                <div class="overflow-hidden h-2 mb-4 text-xs flex rounded bg-orange-200">
                    <div style={{"width": percent + "%" }} class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-500"></div>
                </div>
            </div>
        </div>
    )
}

export default ProgressBar