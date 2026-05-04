import { type BalancesType, type GroupMemberType, type MinimizedDebtType } from '../Types';
import { getAvatarBgClass } from '../utils/avatar';
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
            await api.post('/splittime/api/update_group_settings', {
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

    const multipleCurrencies = Object.keys(byCurrency).length > 1;

    return (
        <div>
            <div className="mb-4">
                <div className="form-check form-switch mb-0">
                    <input
                        className="form-check-input"
                        type="checkbox"
                        role="switch"
                        id="minimize-balances-switch"
                        checked={minimize_balances_setting}
                        onChange={handleToggle}
                    />
                    <label className="form-check-label small fw-medium text-secondary" htmlFor="minimize-balances-switch">
                        Minimize transactions
                    </label>
                </div>
            </div>

            {Object.keys(byCurrency).length === 0 ? (
                <div className="text-center py-5">
                    <i className="bi bi-check-circle-fill display-4 d-block mb-3 text-success opacity-75"></i>
                    <p className="fs-5 fw-semibold mb-1 text-success">All settled up!</p>
                    <small className="text-secondary">No outstanding balances</small>
                </div>
            ) : (
                Object.entries(byCurrency).map(([currency, entries]) => (
                    <div key={currency} className="mb-4">
                        {multipleCurrencies && (
                            <div className="expense-month-heading d-flex align-items-center gap-2 mb-2 pb-2">
                                {currency}
                            </div>
                        )}
                        <div className="d-flex flex-column gap-2">
                            {entries.map((debt, i) => {
                                const fromName = getUsername(debt.from_user);
                                const toName = getUsername(debt.to_user);
                                return (
                                    <div key={i} className="card border shadow-sm rounded-3">
                                        <div className="card-body p-3">
                                            <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', alignItems: 'center', gap: '16px' }}>
                                                <div className="d-flex align-items-center justify-content-between">
                                                    <div className="d-flex align-items-center gap-2">
                                                        <div className={`avatar-md rounded-circle text-white d-flex align-items-center justify-content-center fw-bold ${getAvatarBgClass(fromName)}`}>
                                                            {fromName.slice(0, 2).toUpperCase()}
                                                        </div>
                                                        <span className="fw-bold small text-dark">{fromName}</span>
                                                    </div>
                                                    <div className="d-flex align-items-center gap-2">
                                                        <i className="bi bi-chevron-right text-secondary small"></i>
                                                        <i className="bi bi-chevron-right text-secondary small"></i>
                                                        <i className="bi bi-chevron-right text-secondary small"></i>
                                                    </div>
                                                </div>
                                                <span className="badge rounded-pill bg-danger-subtle text-danger-emphasis fw-semibold px-3 py-2">
                                                    {currency} {debt.amount.toFixed(2)}
                                                </span>
                                                <div className="d-flex align-items-center justify-content-between">
                                                    <div className="d-flex align-items-center gap-2">
                                                        <i className="bi bi-chevron-right text-secondary small"></i>
                                                        <i className="bi bi-chevron-right text-secondary small"></i>
                                                        <i className="bi bi-chevron-right text-secondary small"></i>
                                                    </div>
                                                    <div className="d-flex align-items-center gap-2">
                                                        <span className="fw-bold small text-dark">{toName}</span>
                                                        <div className={`avatar-md rounded-circle text-white d-flex align-items-center justify-content-center fw-bold ${getAvatarBgClass(toName)}`}>
                                                            {toName.slice(0, 2).toUpperCase()}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                ))
            )}
        </div>
    );
}

export default GroupDetailsBalances;