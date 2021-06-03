const Value = require("../models/value");
const Controller = require("./controller");

class ColorsController extends Controller {

    constructor(labels, defaultColorList) {
        super()
        
        this.labels = labels
        this.values = defaultColorList.map((color) => new Value(color))
    }
}

module.exports = ColorsController