const Controller = require("./controller");
const BlockController = require("./block");
const InputController = require("./input");

/**
 * A SelectBlockOption
 * @typedef {Object} Prese
 * @property {Object} block - block of preset
 * @property {string} name - The name of option
 * @property {string} type - The type return of option
 */

class SelectBlockController extends Controller {

    /**
     * @param {Object[]} presets
     * @param {int} defaultValues
     */
    constructor(presets, defaultIndex = 0, onChange = () => {}) {
        super('selectBlock');

        this.presets = presets
        this.blockController = this.buildPreset(this.presets[defaultIndex])
        this.onChange = onChange
    }

    buildPreset(preset) {
        if (preset.value) {
            return new InputController(preset.value, { container: false, onlyNumber: preset.onlyNumber})
        }
        return new BlockController(preset.name, preset.type, preset.block, preset.options)
    }

    usePreset(preset) {
        this.blockController = this.buildPreset(preset)
        console.log('test')
        this.onChange(preset)
    }

    get controllerType() {
        if (this.blockController instanceof InputController ) return 'input'
        if (this.blockController instanceof BlockController) return 'block'
        return null
    }
}

module.exports = SelectBlockController