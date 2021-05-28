const Block = require("./block")

const TYPE = 'variable'

class Variable extends Block {

    constructor(name) {
        super(TYPE)

        this.name = name
    }

    build(context) {
        const variable = context.variables[this.name]
        if (variable) return variable.name
        return null
    }

    return(context) {
        const variable = context.variables[this.value]
        if (variable) return variable
        return 'unknown'
    }

    write() {
        return {
            'type': TYPE,
            'name': this.name
        }
    }

    static read({ type, name }) {
        if (type !== TYPE) return

        return new Variable(name)
    }
}

module.exports = Variable