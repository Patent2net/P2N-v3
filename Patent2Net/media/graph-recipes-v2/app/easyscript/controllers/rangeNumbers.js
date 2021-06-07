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

    blur() {
        super.blur()
        const minCtrlr = this.rangeNumbersController.minInputController
        const maxCtrlr = this.rangeNumbersController.maxInputController

        if ( this.min && maxCtrlr.value < minCtrlr.value ) {
            maxCtrlr.value = minCtrlr.value
        }
        if ( !this.min && minCtrlr.value > maxCtrlr.value ) {
            minCtrlr.value = maxCtrlr.value
        }
    }
}


module.exports = RangeNumbersController