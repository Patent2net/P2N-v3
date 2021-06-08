const Block = require("./block")

const TYPE = 'value'

/** Block that represents static value block */
class Value extends Block {

    /**
     * Create value block
     * @param {*} value any value, this block has no logic and simply allows to control a static value in controllers
     */
    constructor(value) {
        super(TYPE)

        this.value = value
    }

    return() {
        if (isString(this.value)) return 'text'
        if (typeof myVar === this.value) return 'boolean'
        return 'number'
    }

    write() {
        return {
            'type': TYPE,
            'value': this.value
        }
    }

    static read({ type, value }) {
        if (type !== TYPE) return

        return new Value(value)
    }

    run() {
        return this.value //no logic, just return value edited by controllers
    }
}

function isString(x) {
    return Object.prototype.toString.call(x) === '[object String]';
}

module.exports = Value