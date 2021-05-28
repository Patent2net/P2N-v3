const easyscript = require('./easyscript');
const Method = require('./blocks/method');
const Math = require('./blocks/math');
const Value = require('./blocks/value');

const context = {
    graph: 'graph', 
    node: 'node',
    size: 'size'
}

const contextv2 = {
    variables: {
        node: {
            type: 'object',
            name: 'node',
            title: 'Noeud'
        },
        size: {
            type: 'number',
            name: 'size',
            title: 'Taille initial'
        }
    },
    methodes: {
        getNodeAttribute: {
            returnType: 'unknown',
            name: 'graph.getNodeAttribute',
            title: 'Récuperer l\'attribut d\'un noeud'
        }
    }
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
        'name': 'div',
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
                                    'value': 20
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

const test = easyscript(data)
const restructured = test.write()

console.log(
    easyscript(restructured).build(context)
)
