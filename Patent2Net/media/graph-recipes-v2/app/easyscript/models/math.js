const Block = require("./block")

const TYPE = "math"

class Math extends Block {

    constructor(block1, signName, block2) {
        super(TYPE)

        this.block1 = block1
        this.block2 = block2
        this.signName = signName
    }

    build(context) {
        return this.block1.build(context) + ` ${Math.getSign(this.signName)} ` + this.block2.build(context)
    }

    return() {
        if (this.block1.return() === this.block2.return()) {
            return this.block1.return()
        }
        return 'unknown'
    }

    write() {
        return {
            'type': TYPE,
            'value': {
                'name': this.signName,
                'values': [
                    this.block1.write(),
                    this.block2.write()
                ]
            }
        }
    }

    static getSign(signName) {
        if (signName === 'add') return '+'
        if (signName === 'sub') return '-'
        if (signName === 'mpy') return '*'
        if (signName === 'div') return '/'
    }

    static read({ type, value }) {
        if (type !== TYPE) return

        const easyscript = require("./../easyscript.js")

        const signName = value.name
        const block1 = easyscript(value.values[0])
        const block2 = easyscript(value.values[1])

        return new Math(block1, signName, block2)
    }
}

module.exports = Math