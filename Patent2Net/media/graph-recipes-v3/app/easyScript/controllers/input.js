const { floor } = require("numeric");
const Value = require("../models/value");
const Controller = require("./controller");

const defaultOptions = { 
    showType: true, // Display the data type in the input
    type: null, // Display a custom unit instead of the type (px, %, km) in this form field. If null, we display the javascript type
    onlyNumber: false, // Allow only numbers in this field
    container: true // Show the box container around the field
}

/**
 * This controller allows the user to change a static value in the code execution
 */
class InputController extends Controller {

    /**
     * 
     * @param {*} defaultValue default value of input
     * @param {*} options display customization, refer to defaultOptions for the list 
     */
    constructor(defaultValue, options = defaultOptions) {
        super('input');
        
        this.block = new Value(defaultValue);
        this.options = Object.assign({}, defaultOptions)
        for (var attrname in options) { this.options[attrname] = options[attrname]; }
    }

    // When the value is modified, it is here that we apply the modifications to the models
    set value(value) {
        console.log(this.options)
        if (this.options.onlyNumber) { // If only number
            if (!isNaN(value)) { // Apply changes only if it is a number
                return this.block.value = Number(value) // the forms return only string values. They must be transformed into numbers for execution
            }
        } else {
            if (!isNaN(value)) {
                return this.block.value = Number(value) // the forms return only string values. They must be transformed into numbers for execution
            }
            return this.block.value = value
        }
    }

    // The view uses this method to retrieve the value of the field
    get value() {
        return this.block.value
    }

    // The view uses this method to retrieve the value displayed in the label type
    get type() {
        return this.options.type ? this.options.type : this.block.return()
    }

    // When you leave the field (abstract method)
    blur() {}

    // When you enter in field
    focus () {}
}

module.exports = InputController
