import React, { useEffect, useState } from 'react';

function GroupDetailsBalances({ groupBalances, groupMembers, groupId, loginParams}) {

    const [balances, setBalances] = useState(groupBalances)

    useEffect(() => {
        setBalances(groupBalances)
        console.log(groupBalances)
    }, [groupBalances]); // This will trigger whenever initialValue changes

    function getUsername(user_id) {
        return groupMembers.find((user) => user.id === parseInt(user_id,10)).username
    }

    return (
        <div>
            { balances && Object.keys(balances).length >=1 ? (
                <ul>
                    { Object.entries(balances).map(([to_user, list_of_debts]) => (
                    <li key={to_user}>
                        { getUsername(to_user) } is owned:
                        <ul>
                        {Object.entries(list_of_debts).map(([from_user, amounts]) =>(
                            <li key={from_user}>
                                by { getUsername(from_user)} :
                                <ul>
                                {Object.entries(amounts).map(([currency, amount]) =>(
                                    <li key={currency}> {currency} : {amount}</li>
                                ))}
                                </ul>
                            </li>
                        ))}
                        </ul>
                    </li>
                    ))}
                </ul>
            ) : (
                <p>No balances found</p>
            )}
            
        </div>
    );
}

export default GroupDetailsBalances;