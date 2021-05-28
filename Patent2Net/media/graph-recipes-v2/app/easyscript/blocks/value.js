const Block = require("./block")

const TYPE = 'value'

class Value extends Block {

    constructor(value, useContext = false) {
        super(TYPE)

        this.value = value
        this.useContext = useContext
    }

    build(context) {
        if (context[this.value] && this.useContext) return context[this.value]
        if (isString(this.value)) return `'${this.value}'`
        return this.value
    }

    return() {
        if (!useContext) {
            if (isString(this.value)) return 'text'
            if (typeof myVar === this.value) return 'boolean'
            return 'number'
        }
        return 'unknown'
    }

    write() {
        return {
            'type': TYPE,
            'value': {
                'value': this.value,
                'useContext': this.useContext
            }
        }
    }

    static read({ type, value }) {
        if (type !== TYPE) return

        return new Value(value.value, !!value.useContext)
    }
}

function isString(x) {
    return Object.prototype.toString.call(x) === '[object String]';
}

module.exports = Value