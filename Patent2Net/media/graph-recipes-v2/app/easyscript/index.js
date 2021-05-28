const easyscript = require('./easyscript');
const Method = require('./blocks/method');
const Math = require('./blocks/math');
const Value = require('./blocks/value');
const Variable = require('./blocks/variable');

// const context = {
//     graph: 'graph', 
//     node: 'node',
//     size: 'size'
// }

const contextv2 = {
    variables: {
        'node': {
            type: 'object',
            name: 'node',
            title: 'Noeud'
        },
        'size': {
            type: 'number',
            name: 'size',
            title: 'Taille initial'
        }
    },
    methods: {
        'getNodeAttribute': {
            returnType: 'unknown',
            name: 'graph.getNodeAttribute',
            title: 'Récuperer l\'attribut d\'un noeud',
            params: [
                {
                    type: 'object',
                    name: 'node',
                    title: 'Noeud'
                },
                {
                    type: 'text',
                    name: 'attribute',
                    tile: 'Nom de l\'attribut'
                }
            ]
        }
    }
}

const getNodeAttribute = new Method(
    'getNodeAttribute', 
    { 
        node: new Variable('node'),
        attribute: new Value('Category') 
    }, 
    'number'
)

const addition = new Math(
    new Variable('size'),
    'add',
    getNodeAttribute
)


console.log(addition.build(contextv2))

const json = addition.write()

console.log(JSON.stringify(json))

const read = easyscript(json)

console.log(read.build(contextv2))

console.log(JSON.stringify(read.write()))

console.log('SAME: ' + (JSON.stringify(json) === JSON.stringify(read.write()) ? 'OUI' : 'NON'))

// const data = {f
//     'type': 'math',
//     'value': {
//         'name': 'div',
//         'values': [
//             {
//                 'type': 'method',
//                 'value': {
//                     'name': 'degree',
//                     'return': 'number'
//                 }
//             },
//             {
//                 'type': 'method',
//                 'value': {
//                     'name': 'getNodeAttribute',
//                     'params': [
//                         {
//                             'name': 'attribue',
//                             'value': {
//                                 'type': 'value',
//                                 'value': {
//                                     'value': 20
//                                 }
//                             }
//                         }
//                     ],
//                     'return': 'number'
//                 },
//             }
//         ]
//     }
// }

// const test = easyscript(data)
// const restructured = test.write()

// console.log(
//     easyscript(restructured).build(context)
// )
