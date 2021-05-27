const Block = require("./block")

const TYPE = 'method'

class Method extends Block {

    constructor(name, params, returnType) {
        super(TYPE)
        
        this.name = name
        this.params = params
        this.returnType = returnType
    }

    build(context) {
        const { graph, node } = context

        const s_param = ((node, params) => {
            if (params && params.length) {
                console.log(params)
                return `${node}, ${Object.values(params).map((val) => val.build(context)).join(', ')}`
            }
            return node
        })(node, this.params)

        return `${graph}.${this.name}(${s_param})`
    }

    return() {
        return this.returnType
    }

    static read({ type, value }) {
        if (type !== TYPE) return

        const name = value.name
        const paramsArray = value.params
        const params = {}
        const returnValue = value.return

        if (paramsArray) {
            for (const param of paramsArray) {
                
                const easyscript = require("../easyscript")
                
                const paramName = param.name
                const paramValue = param.value

                params[paramName] = easyscript(paramValue)
            }
        }

        return new Method(name, params, returnValue)
    }
}

module.exports = Method