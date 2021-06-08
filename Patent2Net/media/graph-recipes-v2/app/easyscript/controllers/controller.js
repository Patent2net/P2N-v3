/**
 * Controllers describe how the view behaves according to the user's actions
 * 
 * It stores one or more block templates that it can modify and restore at runtime.
 * 
 * Each controller is associated with a view (./easyscript/views)
 * 
 */
class Controller {
    
    constructor(name) {
        this.name = name
    }
}

module.exports = Controller;