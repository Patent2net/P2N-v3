const Logic = require("./blocks/logic")
const Math = require("./blocks/math")
const Value = require("./blocks/value")
const Method = require("./blocks/method")

function easyscript(data) {

    const readers = [
        Math.read,
        Method.read,
        Value.read,
        Logic.read
    ]

    for ( read of readers ) {
        const result = read(data, easyscript)
        if (result) return result
    }
}


module.exports = easyscript