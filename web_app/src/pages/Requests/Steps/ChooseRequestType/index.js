import React from 'react';
import RequestTypeChoice from './RequestTypeChoise';

const ChooseRequestType = ({requestType, setRequestType}) => (
    <div className="grid grid-cols-2 gap-3">
        <RequestTypeChoice
            type="request"
            requestType={requestType}
            setRequestType={setRequestType}
            title="CQL request"
            description="Make one or more CQL requests on the basis of European patents"
        />
        <RequestTypeChoice 
            type="csv"
            requestType={requestType}
            setRequestType={setRequestType}
            title="CSV file"
            description="Using a patent list from a CSV file"
        />
    </div>
)

export default ChooseRequestType;