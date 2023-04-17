const Value = require("../models/value");
const Controller = require("./controller");

/**
 * Controller used to change a color list
 */
class ColorsController extends Controller {

    /**
     * Create ColorsController
     * @param {string[]} labels label associated with each color. The labels must correspond to their purpose in the code execution
     * @param {string[]} defaultColorList default color list in hex format
     */
    constructor(labels, defaultColorList) {
        super('colors')
        
        this.labels = labels
        this.values = defaultColorList.map((color) => new Value(color))
    }
}

module.exports = ColorsController