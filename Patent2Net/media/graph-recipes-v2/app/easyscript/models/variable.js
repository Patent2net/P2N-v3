const Block = require("./block")

const TYPE = 'variable'

class Variable extends Block {

    constructor(name) {
        super(TYPE)

        this.name = name
    }

    build(renderOptions) {
        const name = renderOptions[this.name]
        if (name) return name
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

    run(context) {
        return context[this.name]
    }
}

module.exports = Variable