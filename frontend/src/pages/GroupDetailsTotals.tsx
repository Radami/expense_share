import React, { useEffect, useState } from 'react';
import {
    Bar,
    BarChart,
    CartesianGrid,
    Cell,
    LabelList,
    ResponsiveContainer,
    XAxis,
    YAxis,
} from 'recharts';

import type { ExpenseType, GroupMemberType } from '../Types';

interface GroupDetailsTotalsProps {
    groupExpenses: ExpenseType[],
    groupMembers: GroupMemberType[],
}

const BAR_COLORS = [
    '#0d6efd', '#6610f2', '#1d5525', '#d63384',
    '#dc3545', '#fd7e14', '#198754', '#20c997', '#0dcaf0',
];

const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
];

const GroupDetailsTotals: React.FC<GroupDetailsTotalsProps> = ({ groupExpenses, groupMembers }) => {
    const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth());
    const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
    const [selectedCurrency, setSelectedCurrency] = useState('');

    const currencies = [...new Set(groupExpenses.map(e => e.currency))];

    useEffect(() => {
        if (currencies.length > 0 && !currencies.includes(selectedCurrency)) {
            setSelectedCurrency(currencies[0]);
        }
    }, [groupExpenses]);

    const filtered = groupExpenses
        .filter(e => e.currency === selectedCurrency)
        .filter(e => {
            const d = new Date(e.creation_date);
            return d.getMonth() === selectedMonth && d.getFullYear() === selectedYear;
        });

    const total = filtered.reduce((sum, e) => sum + e.amount, 0);

    const byPayee: Record<string, number> = {};
    for (const member of groupMembers) {
        byPayee[member.username] = 0;
    }
    for (const e of filtered) {
        byPayee[e.payee] = (byPayee[e.payee] ?? 0) + e.amount;
    }

    const chartData = Object.entries(byPayee).map(([name, amount]) => ({
        name,
        amount,
        percentage: total > 0 ? (amount / total) * 100 : 0,
    }));

    return (
        <div>
            <div className="d-flex flex-wrap gap-3 mb-4">
                {currencies.length > 0 && (
                    <select
                        className="form-select w-auto"
                        value={selectedCurrency}
                        onChange={e => setSelectedCurrency(e.target.value)}
                    >
                        {currencies.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                )}
                <div className="d-flex align-items-center gap-1">
                    <button
                        className="btn btn-sm btn-outline-secondary"
                        onClick={() => {
                            if (selectedMonth === 0) {
                                setSelectedMonth(11)
                                setSelectedYear(y => y - 1)
                            } else {
                                setSelectedMonth(m => m - 1)}}
                            }
                    >&lt;</button>
                    <span className="mx-2 fw-semibold text-center" style={{ width: '90px', display: 'inline-block' }}>{months[selectedMonth]}</span>
                    <button
                        className="btn btn-sm btn-outline-secondary"
                        onClick={() => {
                            if (selectedMonth === 11) {
                                setSelectedMonth(0)
                                setSelectedYear(y => y + 1)
                            } else {
                                setSelectedMonth(m => m + 1)
                            }
                        }}
                    >&gt;</button>
                </div>
                <div className="d-flex align-items-center gap-1">
                    <button
                        className="btn btn-sm btn-outline-secondary"
                        onClick={() => setSelectedYear(y => y - 1)}
                    >&lt;</button>
                    <span className="mx-2 fw-semibold">{selectedYear}</span>
                    <button
                        className="btn btn-sm btn-outline-secondary"
                        onClick={() => setSelectedYear(y => y + 1)}
                    >&gt;</button>
                </div>
            </div>

            {total > 0 ? (
                <>
                    <p className="text-muted mb-3">
                        Total: <strong>{selectedCurrency} {total.toFixed(2)}</strong>
                    </p>
                    <ResponsiveContainer width="100%" height={320}>
                        <BarChart data={chartData} margin={{ top: 28, right: 20, left: 10, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} />
                            <XAxis dataKey="name" />
                            <YAxis
                                tickFormatter={v => `${selectedCurrency} ${v}`}
                                width={90}
                            />
                            <Bar dataKey="amount" radius={[4, 4, 0, 0]}>
                                {chartData.map((_entry, i) => (
                                    <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />
                                ))}
                                <LabelList
                                    dataKey="amount"
                                    position="insideTop"
                                    fill="white"
                                    formatter={((v: unknown) => {
                                        const n = Number(v);
                                        return n > 0 ? `${selectedCurrency} ${n.toFixed(2)}` : '';
                                    }) as never}
                                />
                                <LabelList
                                    dataKey="percentage"
                                    position="top"
                                    formatter={((v: unknown) => {
                                        const n = Number(v);
                                        return n > 0 ? `${n.toFixed(1)}%` : '';
                                    }) as never}
                                />
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </>
            ) : (
                <p className="text-muted">No expenses for this period.</p>
            )}
        </div>
    );
};

export default GroupDetailsTotals;
