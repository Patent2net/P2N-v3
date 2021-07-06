import classNames from 'classnames';
import React from 'react';

const RequestTypeChoice = ({type, requestType, setRequestType, title, description}) => {

    const select = React.useCallback(() => {
        setRequestType(type)
        console.log(type)
    }, [setRequestType, type]);

    const isSelected = React.useMemo(() => type === requestType, [requestType, type]);

    return (
        <div
            onClick={select}
            className={classNames({
                "cursor-pointer box-border rounded p-3 border-2 border-indigo-600": isSelected,
                "cursor-pointer box-border rounded p-3 border-2 border-gray-300 opacity-50": !isSelected,
            })} 
            role="radio" aria-checked="false" tabindex="-1">
            <div className="flex items-center justify-between w-full">
                <div className="flex items-center">
                    <div className="text-sm">
                        <p className="font-medium text-indigo-600">{title}</p>
                        <span className="inline text-gray-800">{description}</span> 
                    </div>
                </div>
            </div>
        </div>
    )
}

export default RequestTypeChoice;