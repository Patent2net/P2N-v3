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
            if (params && Object.values(params).length) {
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

    write() {
        const params = this.params
        const paramsArray = []

        for ( const key in params) {
            const param = params[key]

            paramsArray.push({
                'name': key,
                'value': param.write()
            })
        }

        const value = {}
        value['name'] = this.name
        if (paramsArray.length > 0) value['params'] = paramsArray
        value['return'] = this.returnType

        return {
            'type': TYPE,
            'value': value
        }
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