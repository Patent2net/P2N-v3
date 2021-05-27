const Block = require("./block")

const TYPE = "math"

class Math extends Block {

    constructor(block1, sign, block2) {
        super(TYPE)

        this.block1 = block1
        this.block2 = block2
        this.sign = sign
    }

    build(context) {
        return this.block1.build(context) + ` ${this.sign} ` + this.block2.build(context)
    }

    return() {
        if (this.block1.return() === this.block2.return()) {
            return this.block1.return()
        }
        return 'unknown'
    }

    static getSign(type) {
        if (type === 'add') return '+'
        if (type === 'sub') return '-'
        if (type === 'mpy') return '*'
        if (type === 'div') return '/'
    }

    static read({ type, value }) {
        if (type !== TYPE) return

        const easyscript = require("./../easyscript.js")

        const sign = Math.getSign(value.name)
        const block1 = easyscript(value.values[0])
        const block2 = easyscript(value.values[1])

        return new Math(block1, sign, block2)
    }
}

module.exports = Math