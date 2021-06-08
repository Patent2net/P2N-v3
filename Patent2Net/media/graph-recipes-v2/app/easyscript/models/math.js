const Block = require("./block")

const TYPE = "math"

/** Block that represents math operation */
class Math extends Block {

    /**
     * Create a math operation block
     * @param {Block} block1 
     * @param {string} signName name of sign operation (add/sub/mpy/div)
     * @param {Block} block2 
     */
    constructor(block1, signName, block2) {
        super(TYPE)

        this.block1 = block1
        this.block2 = block2
        this.signName = signName
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

    run(context) {
        result1 = this.block1.run(context) 
        result2 = this.block2.run(context)
        
        if (this.signName === 'add') return result1 + result2
        if (this.signName === 'sub') return result1 - result2
        if (this.signName === 'mpy') return result1 * result2
        if (this.signName === 'div') return result1 / result2

    }
}

module.exports = Math