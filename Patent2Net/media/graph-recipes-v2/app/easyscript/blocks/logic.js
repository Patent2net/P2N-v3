const Block = require("./block")

const TYPE = 'logic'

class Logic extends Block {

    constructor(block1, logic, block2) {
        super(TYPE)

        this.block1 = block1
        this.block2 = block2
        this.logic = logic
    }

    build(context) {
        return this.block1.build(context) + ` ${this.logic} ` + this.block2.build(context)
    }

    return() {
        return 'unknown'
    }

    static getLogic(type) {
        if (type === 'AND') return '&&'
        if (type === 'OR') return '||'
    }

    static read({ type, value }) {
        if (type !== TYPE) return

        const easyscript = require("../easyscript")

        const logic = Logic.getLogic(value.name)
        const block1 = easyscript(value.values[0])
        const block2 = easyscript(value.values[1])

        return new Logic(block1, logic, block2)
    }
}

module.exports = Logic