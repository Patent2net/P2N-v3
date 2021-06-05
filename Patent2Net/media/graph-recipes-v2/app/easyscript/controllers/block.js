const Controller = require("./controller");

class BlockController extends Controller {

    constructor(name, type, block) {
        super('block');

        this.name = name
        this.type = type
        this.block = block
    }
}

module.exports = BlockController