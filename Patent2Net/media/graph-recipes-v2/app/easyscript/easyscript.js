const Logic = require("./models/logic")
const Math = require("./models/math")
const Value = require("./models/value")
const Method = require("./models/method")
const Variable = require("./models/variable")

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