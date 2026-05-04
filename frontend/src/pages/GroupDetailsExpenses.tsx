import React, { useEffect, useState } from 'react';
import { type ExpenseType, type GroupMemberType } from '../Types';
import api from '../utils/axios';
import { getAvatarBgClass } from '../utils/avatar';

interface GroupDetailsExpensesProps {
    group_expenses: ExpenseType[],
    group_members: GroupMemberType[],
    group_id: string,
}


const MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
];

const GroupDetailsExpenses: React.FC<GroupDetailsExpensesProps> = ({ group_expenses }) => {
    const [expenses, setExpenses] = useState(group_expenses);
    const [headers, setHeaders] = useState<Record<number, string>>({});

    useEffect(() => {
        setExpenses(group_expenses);
        setHeaders(processMonthHeaders(group_expenses));
    }, [group_expenses]);

    function getMonthFromDate(datetime: string): string {
        return MONTH_NAMES[new Date(datetime).getUTCMonth()];
    }

    function getMonthAndYearFromDate(datetime: string): string {
        const dt = new Date(datetime);
        return `${getMonthFromDate(datetime)} ${dt.getUTCFullYear()}`;
    }

    function getDayFromDate(datetime: string): number {
        return new Date(datetime).getUTCDate();
    }

    function processMonthHeaders(list: ExpenseType[]): Record<number, string> {
        if (!list || list.length === 0) return {};
        const mapping: Record<number, string> = {};
        mapping[0] = getMonthAndYearFromDate(list[0].creation_date);
        for (let i = 1; i < list.length; i++) {
            if (getMonthFromDate(list[i].creation_date) !== getMonthFromDate(list[i - 1].creation_date)) {
                mapping[i] = getMonthAndYearFromDate(list[i].creation_date);
            }
        }
        return mapping;
    }

    function deleteExpense(id: string) {
        api.post('http://localhost:8000/splittime/api/delete_group_expense', { expense_id: id })
            .then(response => {
                if (response.status === 200) {
                    const updated = expenses.filter(e => e.id !== id);
                    setExpenses(updated);
                    setHeaders(processMonthHeaders(updated));
                }
            })
            .catch(error => console.error('Error deleting expense', error));
    }

    return (
        <div>
            {expenses && expenses.length > 0 ? (
                expenses.map((e, index) => (
                    <React.Fragment key={e.id}>
                        {headers[index] && (
                            <div className="expense-month-heading d-flex align-items-center gap-2 mt-3 mb-2 pb-2">
                                <i className="bi bi-receipt"></i>
                                {headers[index]}
                            </div>
                        )}
                        <div className="card border shadow-sm rounded-4 mb-2">
                            <div className="card-body p-3">
                                <div className="d-flex align-items-center gap-3">
                                    <div className="date-badge rounded-3 text-white d-flex flex-column align-items-center justify-content-center flex-shrink-0">
                                        <span className="fw-bold lh-1">{getDayFromDate(e.creation_date)}</span>
                                        <span className="date-badge-month">
                                            {getMonthFromDate(e.creation_date).slice(0, 3).toUpperCase()}
                                        </span>
                                    </div>
                                    <div className="flex-grow-1">
                                        <h6 className="fw-bold mb-1 text-dark">{e.name}</h6>
                                        <div className="d-flex flex-wrap align-items-center gap-2">
                                            <div className={`avatar-sm rounded-circle text-white d-flex align-items-center justify-content-center fw-bold ${getAvatarBgClass(e.payee)}`}>
                                                {e.payee.slice(0, 2).toUpperCase()}
                                            </div>
                                            <span className="text-secondary small fw-medium">{e.payee}</span>
                                            <span className="text-secondary small">paid</span>
                                            <span className="badge rounded-pill badge-amount fw-semibold px-3 py-2">
                                                {e.currency} {e.amount.toFixed(2)}
                                            </span>
                                            {e.you_owe > 0 && (
                                                <>
                                                    <span className="text-secondary small">· You owe</span>
                                                    <span className="badge rounded-pill bg-danger-subtle text-danger-emphasis fw-semibold px-3 py-2">
                                                        {e.currency} {e.you_owe.toFixed(2)}
                                                    </span>
                                                </>
                                            )}
                                        </div>
                                    </div>
                                    <button
                                        className="btn btn-link text-secondary p-2 rounded-2 delete-btn-hover flex-shrink-0"
                                        onClick={() => deleteExpense(e.id)}
                                        title="Delete expense"
                                    >
                                        <i className="bi bi-trash3"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </React.Fragment>
                ))
            ) : (
                <div className="text-center py-5 text-secondary">
                    <i className="bi bi-receipt-cutoff display-4 d-block mb-3 opacity-25"></i>
                    <p className="fs-5 fw-medium mb-1">No expenses yet</p>
                    <small>Add your first expense to get started</small>
                </div>
            )}
        </div>
    );
};

export default GroupDetailsExpenses;