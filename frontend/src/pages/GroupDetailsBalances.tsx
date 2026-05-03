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

type DebtEntry = {
    from_user: number;
    to_user: number;
    currency: string;
    amount: number;
};

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

    function getRawDebts(): DebtEntry[] {
        const debts: DebtEntry[] = [];
        for (const [creditor_id, debtors] of Object.entries(group_balances)) {
            for (const [debtor_id, amounts] of Object.entries(debtors)) {
                for (const [currency, amount] of Object.entries(amounts)) {
                    if (amount > 0) {
                        debts.push({
                            from_user: Number(debtor_id),
                            to_user: Number(creditor_id),
                            currency,
                            amount,
                        });
                    }
                }
            }
        }
        return debts;
    }

    const debts: DebtEntry[] = minimize_balances_setting ? group_minimized_balances : getRawDebts();

    const byCurrency: Record<string, DebtEntry[]> = {};
    for (const debt of debts) {
        if (!byCurrency[debt.currency]) byCurrency[debt.currency] = [];
        byCurrency[debt.currency].push(debt);
    }

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

            {Object.keys(byCurrency).length === 0 ? (
                <p>All settled up!</p>
            ) : (
                Object.entries(byCurrency).map(([currency, entries]) => (
                    <div key={currency} className="mb-3">
                        <h6 className="text-muted text-uppercase mb-2">{currency}</h6>
                        <ul className="list-unstyled mb-0">
                            {entries.map((debt, i) => (
                                <li key={i} className="mb-1">
                                    <strong>{getUsername(debt.from_user)}</strong>
                                    {' → '}
                                    <strong>{getUsername(debt.to_user)}</strong>
                                    {': '}
                                    {debt.amount.toFixed(2)}
                                </li>
                            ))}
                        </ul>
                    </div>
                ))
            )}
        </div>
    );
}

export default GroupDetailsBalances;
