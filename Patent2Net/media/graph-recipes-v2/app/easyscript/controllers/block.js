const Controller = require("./controller");

class BlockController extends Controller {

    constructor(name, type) {
        super();

        this.name = name
        this.type = type
    }
}

module.exports = BlockController