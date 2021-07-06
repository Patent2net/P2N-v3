import React from 'react';
import classnames from 'classnames';

const Step = ({ children, title, id, focusID, setFocusID, nextStep, isValid = true, isLastStep = false}) => {

    const takeFocus = React.useCallback(() => {
        setFocusID(id)
    }, [setFocusID, id])

    const isFocused = React.useMemo(() => focusID === id, [focusID, id]);
    const isNextStep = React.useMemo(() => focusID < id, [focusID, id])


    return (
        <section className="text-base">
            <div 
                className={classnames("p-4 border", isFocused ? "bg-indigo-600 text-white" : "bg-gray-200")}
                onClick={() => {
                    if (!isNextStep) takeFocus()
                }}
            >
                <p className="font-semibold">{title}</p>
            </div>
            <div 
                className={classnames("border", {
                    "opacity-50": !isFocused,
                    "hidden": isNextStep
                })}
            >
                <div
                    className="p-4"
                    onClick={takeFocus}
                >
                    {children}
                </div>
                <div className={classnames("p-4 flex justify-end", {
                    "hidden": !isFocused
                })}>
                    <button 
                        className={classnames("focus:shadow-outline focus:outline-none px-8 py-2 rounded-md font-semibold text-white cursor-pointer flex flex-row", {
                            "bg-indigo-500 ": isValid,
                            "bg-gray-300": !isValid
                        })}
                        onClick={() => nextStep(isLastStep)}
                        disabled={!isValid}
                    >
                        {isLastStep ? "Submit" : "Validate"}
                    </button>
                </div>
            </div>

        </section>
    )

}

export default Step;