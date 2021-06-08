const Block = require("./block")

const TYPE = 'method'

/** Block that represents method block */
class Method extends Block {

    /**
     * Create a method block
     * @param {string} name name of method, this name was used as unique key in run method to get javascript function in context
     * @param {Object} params parameter identifier associated with the parameter value, 
     */
    constructor(name, params) {
        super(TYPE)
        this.name = name
        this.params = params
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
        const { method, params_id } = context[this.name] // Get js method with key in context, get params
        if (method) { // If js method found in context
            const param = params_id.map((param_id) => this.params[param_id] ? this.params[param_id].run(context) : null) // Get the value of the parameters used by the js method
            method(...param) // Run js method with parameter values
        }
    }
}

module.exports = Method