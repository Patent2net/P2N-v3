const easyscript = require('./easyscript');
const Method = require('./blocks/method');
const Math = require('./blocks/math');
const Value = require('./blocks/value');

const context = {
    graph: 'graph', 
    node: 'node',
    size: 'size'
}

const getNodeAttribute = new Method(
    'getNodeAttribute', 
    { attribute: new Value('size', true) }, 
    'number'
)

const addition = new Math(
    new Value('size', true),
    '+',
    getNodeAttribute
).build(context)


const data = {
    'type': 'math',
    'value': {
        'name': 'add',
        'values': [
            {
                'type': 'method',
                'value': {
                    'name': 'degree',
                    'return': 'number'
                }
            },
            {
                'type': 'method',
                'value': {
                    'name': 'getNodeAttribute',
                    'params': [
                        {
                            'name': 'attribue',
                            'value': {
                                'type': 'value',
                                'value': {
                                    'value': 'size',
                                    'useContext': true
                                }
                            }
                        }
                    ],
                    'return': 'number'
                },
            }
        ]
    }
}

console.log(
    easyscript(data).build(context)
)