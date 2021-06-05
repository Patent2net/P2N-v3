const { floor } = require("numeric");
const Value = require("../models/value");
const Controller = require("./controller");

const defaultOptions = { 
    showType: true,
    type: null,
    onlyNumber: false,
    container: true
}

class InputController extends Controller {

    constructor(defaultValue, options = defaultOptions) {
        super('input');
        
        this.block = new Value(defaultValue);
        this.options = Object.assign({}, defaultOptions)
        for (var attrname in options) { this.options[attrname] = options[attrname]; }
    }

    set value(value) {
        console.log(this.options)
        if (this.options.onlyNumber) {
            if (!isNaN(value)) {
                return this.block.value = Number(value)
            }
        } else {
            if (!isNaN(value)) {
                return this.block.value = Number(value)
            }
            return this.block.value = value
        }
    }

    get value() {
        return this.block.value
    }

    get type() {
        return this.options.type ? this.options.type : this.block.return()
    }
}

module.exports = InputController
