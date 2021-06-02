const Controller = require("./controller");

class InputController extends Controller {

    constructor(defaultBlock, context) {
        super(context);
        
        this.block = defaultBlock;
    }

    getValue() {
        return this.block.value;
    }

    setValue(value) {
        this.block.value = value;
    }
    
    getReturnType() {
        return this.block.return(this.context)
    }
}

module.exports = InputController
