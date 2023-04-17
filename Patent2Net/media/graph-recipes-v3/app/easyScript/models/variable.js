const Block = require("./block")

const TYPE = 'variable'

/** Block that represents variable block */
class Variable extends Block {

    /**
     * Create variable block
     * @param {string} name Key used by the variable to retrieve its value in the context
     */
    constructor(name) {
        super(TYPE)

        this.name = name
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

    run(context) {
        return context[this.name]
    }
}

module.exports = Variable