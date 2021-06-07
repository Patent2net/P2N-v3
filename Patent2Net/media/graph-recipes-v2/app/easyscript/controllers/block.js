const Controller = require("./controller");

const defaultOptions = {showType: true}
class BlockController extends Controller {

    constructor(name, type, block, options=defaultOptions) {
        super('block');

        this.name = name
        this.type = type
        this.block = block
        this.options = options
    }
}

module.exports = BlockController