const Controller = require("./controller");

const defaultOptions = {showType: true}

/**
 * Allows you to create a predefined block
 */
class BlockController extends Controller {

    /**
     * 
     * @param {string} name name used by the preset
     * @param {*} type type returned by the preset
     * @param {*} block the block preset model
     * @param {*} options display options to use when rendering, refer to defaultOptions
     */
    constructor(name, type, block, options=defaultOptions) {
        super('block');

        this.name = name
        this.type = type
        this.block = block
        this.options = options
    }
}

module.exports = BlockController