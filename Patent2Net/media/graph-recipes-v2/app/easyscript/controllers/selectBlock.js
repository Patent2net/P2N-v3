const Controller = require("./controller");
const BlockController = require("./block");
const InputController = require("./input");

/**
 * A number, or a string containing a number.
 * @typedef {Object} Preset
 * @property {string} name name displayed in the select drop-down list and on the selected block
 * @property {string} type type of data returned by the preset
 * @property {Object} [block] modele block used for code execution if selected
 * @property {Object} [options] controller block options
 * @property {boolean} [value] if you set a value, block and options was ignore and add an input option in select
 * 
 */


/**
 * the SelectBlockController allows to choose between a list of predefined controllers
 * the value of this block is thus extracted from the selected controller
 * 
 * Controllers are generated directly from the class. We will place in parameter a list
 * of preset that follow the format {Preset}
 * 
 * 2 types of controllers can be created now: BlockController and InputController
 * (See the rules used in {Preset})
 */
class SelectBlockController extends Controller {

    /**
     * @param {Object} presets list of preset
     * @param {*} defaultIndex default preset index used
     * @param {*} onChange method call wehn new element was selected
     */
    constructor(presets, defaultIndex = 0, onChange = () => {}) {
        super('selectBlock');

        this.presets = presets
        this.blockController = this.buildPreset(this.presets[defaultIndex]) // the block controller contains the controller that contains the final value used for code execution
        this.onChange = onChange
    }

    /**
     * Allows to transform a preset into a controller to be rendered on screen
     * @param {Preset} preset 
     * @returns {Controller}
     */
    buildPreset(preset) {
        if (preset.value) {
            return new InputController(preset.value, { container: false, onlyNumber: preset.onlyNumber})
        }
        return new BlockController(preset.name, preset.type, preset.block, preset.options)
    }

    /**
     * Allows you to select a preset
     * @param {Preset} preset 
     */
    usePreset(preset) {
        this.blockController = this.buildPreset(preset)
        console.log('test')
        this.onChange(preset)
    }

    /**
     * Get the type of controller selected and to be displayed, if value has been defined in the constructor, it is an input controller that is used
     */
    get controllerType() {
        if (this.blockController instanceof InputController ) return 'input'
        if (this.blockController instanceof BlockController) return 'block'
        return null
    }
}

module.exports = SelectBlockController