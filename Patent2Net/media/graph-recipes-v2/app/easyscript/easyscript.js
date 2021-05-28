const Logic = require("./blocks/logic")
const Math = require("./blocks/math")
const Value = require("./blocks/value")
const Method = require("./blocks/method")
const Variable = require("./blocks/variable")

function easyscript(data) {

    const readers = [
        Math.read,
        Method.read,
        Value.read,
        Logic.read,
        Variable.read
    ]

    for ( read of readers ) {
        const result = read(data, easyscript)
        if (result) return result
    }
}


module.exports = easyscript