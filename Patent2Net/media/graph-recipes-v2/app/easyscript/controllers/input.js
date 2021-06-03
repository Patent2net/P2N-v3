const { floor } = require("numeric");
const Value = require("../models/value");
const Controller = require("./controller");

const defaultOptions = { 
    showType: true,
    onlyNumber: false,
    container: true
}

class InputController extends Controller {

    constructor(defaultValue, options = defaultOptions, context) {
        super(context);
        
        this.block = new Value(defaultValue);
        this.options = Object.assign({}, defaultOptions)
        for (var attrname in options) { this.options[attrname] = options[attrname]; }
    }

    set value(value) {
        if (this.options.onlyNumber) {
            if (!isNaN(value)) {
                this.block.value = Number(value)
            }
        } else {
            this.block.value = value
        }
    }

    get value() {
        return this.block.value
    }

    get type() {
        return this.block.return(this.context)
    }
}

module.exports = InputController
