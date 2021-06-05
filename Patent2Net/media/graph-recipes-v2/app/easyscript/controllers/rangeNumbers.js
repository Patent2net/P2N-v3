const Controller = require("./controller");
const InputController = require("./input");

const defaultOptions = { showType: false, onlyNumber: true }

class RangeNumbersController extends Controller {

    constructor(defaultMin, defaultMax, options) {
        super('rangeNumbers');

        this.options = Object.assign({}, defaultOptions)
        for (var attrname in options) { this.options[attrname] = options[attrname]; }
        
        this.minInputController = new RangeInputController(defaultMin, this.options, this, true)
        this.maxInputController = new RangeInputController(defaultMax, this.options, this, false)
    }

    get type() {
        return this.minInputController.type
    }
}


class RangeInputController extends InputController {

    constructor(defaultValue, inputOptions, rangeNumbersController, min) {
        super(defaultValue, inputOptions)

        this.rangeNumbersController = rangeNumbersController
        this.min = min
    }

    get value() {
        return super.value;
    }

    set value(value) {
        value = super.value = value
        const minCtrlr = this.rangeNumbersController.minInputController
        const maxCtrlr = this.rangeNumbersController.maxInputController

        if ( this.min && maxCtrlr.value < value ) {
            maxCtrlr.value = value
        }
        if ( !this.min && minCtrlr.value > value ) {
            minCtrlr.value = value
        }
    }
}


module.exports = RangeNumbersController