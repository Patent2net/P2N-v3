const Controller = require("./controller");
const InputController = require("./input");

class RangeNumbersController extends Controller {

    constructor(defaultMinBlock, defaultMaxBlock, options, context) {
        super(props);

        this.minInputController = new InputController(defaultMinBlock, context)
        this.maxInputController = new InputController(defaultMaxBlock, context)
        this.options = options

        // this.minInputController.setInputValue = this.minInputController.setValue
        // this.minInputController.setValue = (value) => {
        //     this.minInputController.setInputValue(value)
        // }

        // this.maxInputController.setInputValue = this.maxInputController.setValue
        // this.maxInputController.setValue = (value) => {
        //     this.maxInputController.setInputValue(value)
        // }
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