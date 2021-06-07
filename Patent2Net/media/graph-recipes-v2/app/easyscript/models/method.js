const Block = require("./block")

const TYPE = 'method'

class Method extends Block {

    constructor(name, params, meta = {}) {
        super(TYPE, meta)
        
        this.name = name
        this.params = params
    }

    build(renderOptions) {
        const { name, params_name } = renderOptions[this.name]

        const s_param = params_name ? 
            `${Object.values(params_name).map((param) => this.params[param.name].build(renderOptions)).join(', ')}`
            : 
            ''

        return `${name}(${s_param})`
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

    run(context) {
        const { method, params_id } = context[this.name]
        if (method) {
            const param = params_id.map((param_id) => this.params[param_id] ? this.params[param_id].run(context) : null)
            console.log(param)
            console.log(method)
            method(...param)
        }
    }
}

module.exports = Method