const { floor } = require("numeric");
const Value = require("../models/value");
const Controller = require("./controller");

const defaultOptions = { 
    showType: true,
    onlyNumber: false
}

class InputController extends Controller {

    constructor(defaultValue, options = defaultOptions, context) {
        super(context);
        
        this.block = new Value(defaultValue);
        this.options = options
    }

    getValue() {
        return this.block.value;
    }

    setValue(value) {
        const prevValue = this.getValue();
        this.block.value = value;
        this.onValueChange(value, prevValue);
    }

    onValueChange(newValue, prevValue) {
        if (this.options.onlyNumber) {
            if (isNaN(newValue)) {
                this.block.value = prevValue
            } else {
                this.block.value = Number(newValue)
            }
        }
    }
    
    getReturnType() {
        return this.block.return(this.context)
    }
}

module.exports = InputController
