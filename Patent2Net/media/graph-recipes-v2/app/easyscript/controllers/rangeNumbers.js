const Controller = require("./controller");
const InputController = require("./input");

const inputOptions = { showType: false, type: 'px', onlyNumber: true }

class RangeNumbersController extends Controller {

    constructor(defaultMin, defaultMax, options, context) {
        super(context);

        this.minInputController = new RangeInputController(defaultMin, inputOptions, context, this, true)
        this.maxInputController = new RangeInputController(defaultMax, inputOptions, context, this, false)
        this.options = options
    }

    get type() {
        return this.minInputController.type
    }
}


class RangeInputController extends InputController {

    constructor(defaultValue, inputOptions, context, rangeNumbersController, min) {
        super(defaultValue, inputOptions, context)

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