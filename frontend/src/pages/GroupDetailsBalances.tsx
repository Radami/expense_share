import Form from 'react-bootstrap/Form';

import { type BalancesType, type GroupMemberType, type MinimizedDebtType } from '../Types';
import api from '../utils/axios';

interface GroupDetailsBalancesProps {
    group_balances: BalancesType,
    group_minimized_balances: MinimizedDebtType[],
    minimize_balances_setting: boolean,
    group_members: GroupMemberType[],
    group_id: string,
    onRefresh: () => void,
}

const GroupDetailsBalances: React.FC<GroupDetailsBalancesProps> = ({
    group_balances,
    group_minimized_balances,
    minimize_balances_setting,
    group_members,
    group_id,
    onRefresh,
}) => {

    function getUsername(user_id: number | string) {
        const user = group_members.find((u) => u.id === Number(user_id));
        return user ? user.username : 'Unknown User';
    }

    async function handleToggle() {
        try {
            await api.post('http://localhost:8000/splittime/api/update_group_settings', {
                group_id,
                minimize_balances_setting: !minimize_balances_setting,
            });
            onRefresh();
        } catch (error) {
            console.error('Failed to update group settings', error);
        }
    }

    const hasRawBalances = group_balances && Object.keys(group_balances).length >= 1;
    const hasMinimizedBalances = group_minimized_balances && group_minimized_balances.length >= 1;

    return (
        <div>
            <div className="d-flex align-items-center mb-3">
                <Form.Check
                    type="switch"
                    id="minimize-balances-switch"
                    label="Minimize transactions"
                    checked={minimize_balances_setting}
                    onChange={handleToggle}
                />
            </div>

            {minimize_balances_setting ? (
                hasMinimizedBalances ? (
                    <ul className="list-unstyled">
                        {group_minimized_balances.map((t, i) => (
                            <li key={i} className="mb-1">
                                <strong>{getUsername(t.from_user)}</strong>
                                {' → '}
                                <strong>{getUsername(t.to_user)}</strong>
                                {': '}
                                {t.currency} {t.amount.toFixed(2)}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>All settled up!</p>
                )
            ) : (
                hasRawBalances ? (
                    <ul>
                        {Object.entries(group_balances).map(([to_user, list_of_debts]) => (
                            <li key={to_user}>
                                {getUsername(to_user)} is owed:
                                <ul>
                                    {Object.entries(list_of_debts).map(([from_user, amounts]) => (
                                        <li key={from_user}>
                                            by {getUsername(from_user)}:
                                            <ul>
                                                {Object.entries(amounts).map(([currency, amount]) => (
                                                    amount > 0 && (
                                                        <li key={currency}>{currency}: {amount.toFixed(2)}</li>
                                                    )
                                                ))}
                                            </ul>
                                        </li>
                                    ))}
                                </ul>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>All settled up!</p>
                )
            )}
        </div>
    );
}

export default GroupDetailsBalances;
