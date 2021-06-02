const Controller = require("./controller");
const InputController = require("./input");

const inputOptions = { showType: false, onlyNumber: true }

class RangeNumbersController extends Controller {

    constructor(defaultMin, defaultMax, options, context) {
        super(context);

        this.minInputController = new InputController(defaultMin, inputOptions, context)
        this.maxInputController = new InputController(defaultMax, inputOptions, context)
        this.options = options

        this.minInputController.onInputValueChange = this.minInputController.onValueChange
        this.minInputController.onValueChange = (newValue, prevValue) => {
            this.minInputController.onInputValueChange(newValue, prevValue)

            if (this.maxInputController.block.value < newValue) this.maxInputController.setValue(newValue)
            
        }

        this.maxInputController.onInputValueChange = this.maxInputController.onValueChange
        this.maxInputController.onValueChange = (newValue, prevValue) => {
            this.maxInputController.onInputValueChange(newValue, prevValue)
            
            if (this.minInputController.block.value > newValue) this.minInputController.setValue(newValue)
        }
    }

    getMinBlock() {
        return this.minInputController.getBlock(block)
    }

    setMinBlock(block) {
        this.minInputController.setBlock(block)
    }


    getMaxBlock() {
        return this.maxInputController.getBlock(block)
    }

    setMaxBlock(block) {
        this.maxInputController.setBlock(block)
    }

}


module.exports = RangeNumbersController