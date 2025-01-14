import React, { useEffect, useState } from 'react';
import { LoginParamsType } from '../Types';

interface GroupDetailsTotalsProps {
    groupTotals: Record<string, number>,
    loginParams: LoginParamsType
}

const GroupDetailsTotals: React.FC<GroupDetailsTotalsProps> = ({ groupTotals, loginParams}) => {
    const [totals, setTotals] = useState(groupTotals)

    useEffect(() => {
        setTotals(groupTotals)
    }, [groupTotals]); // This will trigger whenever initialValue changes

    return (
        <div>
            { totals && Object.keys(totals).length >= 1 ?
             Object.entries(totals).map(([key, value]) => (
                <div key={key} className="container">
                     <p><strong>{key}:</strong> {value}</p>
                </div>
            
            )): (<p>No totals found</p>)}
        </div>
    );
}

export default GroupDetailsTotals;