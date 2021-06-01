const Block = require("./block")

const TYPE = 'method'

class Method extends Block {

    constructor(name, params, meta = {}) {
        super(TYPE, meta)
        
        this.name = name
        this.params = params
    }

    build(context) {
        const method = context.methods[this.name]


        const s_param = ((method, params) => {
            if (method.params) {
                return `${Object.values(method.params).map((param) => params[param.name].build(context)).join(', ')}`
            }
            return ''
        })(method, this.params)

        return `${method.name}(${s_param})`
    }

    return(context) {
        const method = context.methods[this.name]
        if (!method) return 'unknows'
        return method.returnType
    }

    write() {
        const params = this.params
        const paramsWrite = {}

        for ( const key in params) {
            const param = params[key]
            paramsWrite[key] = param.write()
        }

        const value = {}
        value['name'] = this.name
        value['params'] = paramsWrite

        return {
            'type': TYPE,
            'value': value
        }
    }

    static read({ type, value }) {
        if (type !== TYPE) return

        const name = value.name
        const params = value.params
        const paramsDecoded = {}

        if (params) {
            for (const key in params) {
                const param = params[key]
                const easyscript = require("../easyscript")
                paramsDecoded[key] = easyscript(param)
            }
        }

        return new Method(name, paramsDecoded)
    }
}

module.exports = Method