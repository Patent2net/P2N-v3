/**
 * The block model represents the different code instructions.
 * 
 * They allow to execute different javascript code depending on the parameters 
 * on which the user can make changes.
 * 
 * The modifications on the blocks are done from the controllers (./easyscript/controllers/) each associated 
 * to a view.
 * 
 */
class Block {

    constructor(type) {
        this.type = type
    }

    /**
     * Get final return type of run
     */
    return() {
        throw new Error('You have to implement the method return!');
    }
    
    /**
     * Method to serialize block
     * A static method read must be created to deseralize data
     */
    write() {
        throw new Error('You have to implement the method write!');
    }

    /**
     * Run block with context
     * @param {Object} context global context of execution
     */
    run(context) {
        throw new Error('You have to implement the method run!');
    }

}

module.exports = Block