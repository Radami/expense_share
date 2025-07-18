import React, { useEffect, useState } from 'react';

interface GroupDetailsTotalsProps {
    groupTotals: Record<string, number>,
}

const GroupDetailsTotals: React.FC<GroupDetailsTotalsProps> = ({ groupTotals }) => {
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