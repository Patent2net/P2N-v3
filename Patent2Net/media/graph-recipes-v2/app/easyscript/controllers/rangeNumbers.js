const Controller = require("./controller");
const InputController = require("./input");

const defaultOptions = { showType: false, onlyNumber: true }

/**
 * Controller used to define a value interval
 * It obliges: minimum value <= maximum value
 */
class RangeNumbersController extends Controller {

    /**
     * 
     * @param {number} defaultMin 
     * @param {number} defaultMax 
     * @param {Object} options options of InputController
     */
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

/**
 * Child object of input controller used in the controller range number
 */
class RangeInputController extends InputController {

    /**
     * Create RangeInputController for RangeNumbersController
     * @param {*} defaultValue defaultValue of InputController
     * @param {Object} inputOptions inputOptions of InputController
     * @param {RangeNumbersController} rangeNumbersController 
     * @param {boolean} min Is this component used for the minimum value of the range number?
     */
    constructor(defaultValue, inputOptions, rangeNumbersController, min) {
        super(defaultValue, inputOptions)

        this.rangeNumbersController = rangeNumbersController
        this.min = min
    }

    // Event called when the user input the field
    blur() {
        super.blur()
        const minCtrlr = this.rangeNumbersController.minInputController
        const maxCtrlr = this.rangeNumbersController.maxInputController

        // This controller is used for the min value of rangeNumber and the max value is smaller than min
        if ( this.min && maxCtrlr.value < minCtrlr.value ) {
            maxCtrlr.value = minCtrlr.value // Set max to min value
        }
        // This controller is used for the max value of rangeNumber and the min value is bigger than max
        if ( !this.min && minCtrlr.value > maxCtrlr.value ) {
            minCtrlr.value = maxCtrlr.value // Set min to max value
        }
    }
}


module.exports = RangeNumbersController