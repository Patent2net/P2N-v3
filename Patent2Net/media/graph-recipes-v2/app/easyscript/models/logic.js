const Block = require("./block")

const TYPE = 'logic'

class Logic extends Block {

    constructor(block1, logicName, block2) {
        super(TYPE)

        this.block1 = block1
        this.block2 = block2
        this.logicName = logicName
    }

    build(renderOptions) {
        return this.block1.build(renderOptions) + ` ${Logic.getLogic(this.logicName)} ` + this.block2.build(renderOptions)
    }

    return() {
        return 'unknown'
    }

    write() {
        return {
            'type': TYPE,
            'value': {
                'name': this.logicName,
                'values': [
                    this.block1.write(),
                    this.block2.write()
                ]
            }
        }
    }

    static getLogic(logicName) {
        if (logicName === 'AND') return '&&'
        if (logicName === 'OR') return '||'
    }

    static read({ type, value }) {
        if (type !== TYPE) return

        const easyscript = require("../easyscript")

        const logicName = value.name
        const block1 = easyscript(value.values[0])
        const block2 = easyscript(value.values[1])

        return new Logic(block1, logicName, block2)
    }

    run(context) {
        result1 = this.block1.run(context) 
        result2 = this.block2.run(context)
        
        if (this.signName === 'AND') return result1 && result2
        if (this.signName === 'OR') return result1 || result2
    }
}

module.exports = Logic