const Block = require("./block")

const TYPE = 'value'

class Value extends Block {

    constructor(value, meta = {}) {
        super(TYPE, meta)

        this.value = value
    }

    build() {
        if (isString(this.value)) return `'${this.value}'`
        return this.value
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
        return this.value
    }
}

function isString(x) {
    return Object.prototype.toString.call(x) === '[object String]';
}

module.exports = Value