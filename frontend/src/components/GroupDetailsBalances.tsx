import { useEffect, useState } from 'react';

import { BalancesType, GroupMemberType, LoginParamsType } from '../Types';

interface GroupDetailsBalancesProps {
    group_balances: BalancesType,
    group_members: GroupMemberType[],
    group_id: string,
    login_params: LoginParamsType,
}

const GroupDetailsBalances: React.FC<GroupDetailsBalancesProps> = ({ group_balances, group_members, group_id, login_params}) => {

    const [balances, setBalances] = useState(group_balances)

    // TODO: fix undefined in getUsername when group member gets removed

    useEffect(() => {
        setBalances(group_balances)
        console.log(group_balances)
    }, [group_balances]); // This will trigger whenever initialValue changes

    function getUsername(user_id: string) {
        const user = group_members.find((user) => user.id === user_id)

        if (user) {
            return user.username;
        }
        // Optionally, return a default value if no user is found
        return "Unknown User";
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