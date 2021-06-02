const Controller = require("./controller");

/**
 * A SelectBlockOption
 * @typedef {Object} SelectBlockOption
 * @property {string} name - The name of option
 * @property {string} type - The type return of option
 * @property {*} create - Functions to create block option
 */

class SelectBlockController extends Controller {

    /**
     * @param {Object} defaultBlock
     * @param {SelectBlockOption[]} options
     */
    constructor(defaultBlock, options) {
        super();
        
        this.block = defaultBlock
        this.options = options
    }
    
}

module.exports = SelectBlockController