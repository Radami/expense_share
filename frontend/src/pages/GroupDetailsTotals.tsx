import React, { useEffect, useState } from 'react';
import {
    Bar, BarChart, CartesianGrid, Cell, LabelList, ResponsiveContainer, XAxis, YAxis,
} from 'recharts';
import type { ExpenseType, GroupMemberType } from '../Types';
import { getAvatarColor } from '../utils/avatar';
import { MONTH_NAMES } from '../utils/constants';

interface GroupDetailsTotalsProps {
    groupExpenses: ExpenseType[],
    groupMembers: GroupMemberType[],
}

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
    for (const member of groupMembers) byPayee[member.username] = 0;
    for (const e of filtered) byPayee[e.payee] = (byPayee[e.payee] ?? 0) + e.amount;

    const chartData = Object.entries(byPayee).map(([name, amount]) => ({
        name,
        amount,
        percentage: total > 0 ? (amount / total) * 100 : 0,
    }));

    const prevMonth = () => {
        if (selectedMonth === 0) { setSelectedMonth(11); setSelectedYear(y => y - 1); }
        else setSelectedMonth(m => m - 1);
    };
    const nextMonth = () => {
        if (selectedMonth === 11) { setSelectedMonth(0); setSelectedYear(y => y + 1); }
        else setSelectedMonth(m => m + 1);
    };

    return (
        <div>
            <div className="d-flex flex-wrap align-items-center gap-2 mb-4">
                {currencies.length > 0 && (
                    <select
                        className="form-select form-select-sm w-auto"
                        value={selectedCurrency}
                        onChange={e => setSelectedCurrency(e.target.value)}
                    >
                        {currencies.map(c => <option key={c} value={c}>{c}</option>)}
                    </select>
                )}
                <div className="d-flex align-items-center gap-1">
                    <button className="btn-nav" onClick={prevMonth}>
                        <i className="bi bi-chevron-left"></i>
                    </button>
                    <span className="fw-semibold small text-center totals-period-label">{MONTH_NAMES[selectedMonth]}</span>
                    <button className="btn-nav" onClick={nextMonth}>
                        <i className="bi bi-chevron-right"></i>
                    </button>
                </div>
                <div className="d-flex align-items-center gap-1">
                    <button className="btn-nav" onClick={() => setSelectedYear(y => y - 1)}>
                        <i className="bi bi-chevron-left"></i>
                    </button>
                    <span className="fw-semibold small text-center totals-period-label">{selectedYear}</span>
                    <button className="btn-nav" onClick={() => setSelectedYear(y => y + 1)}>
                        <i className="bi bi-chevron-right"></i>
                    </button>
                </div>
            </div>

            {total > 0 ? (
                <>
                    <p className="small text-secondary mb-3">
                        Total: <strong className="text-dark">{selectedCurrency} {total.toFixed(2)}</strong>
                    </p>
                    <div className="card border shadow-sm rounded-3 px-3 pt-4 pb-3">
                        <ResponsiveContainer width="100%" height={320}>
                            <BarChart data={chartData} margin={{ top: 28, right: 16, left: 8, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ddd5c8" />
                                <XAxis dataKey="name" tick={{ fontSize: 12, fill: '#9a9088' }} axisLine={false} tickLine={false} />
                                <YAxis
                                    tickFormatter={v => `${selectedCurrency} ${v}`}
                                    width={90}
                                    tick={{ fontSize: 11, fill: '#9a9088' }}
                                    axisLine={false}
                                    tickLine={false}
                                />
                                <Bar dataKey="amount" radius={[6, 6, 0, 0]}>
                                    {chartData.map((entry) => (
                                        <Cell key={entry.name} fill={getAvatarColor(entry.name)} />
                                    ))}
                                    <LabelList
                                        dataKey="amount"
                                        position="insideTop"
                                        fill="white"
                                        style={{ fontSize: 11, fontWeight: 700 }}
                                        formatter={((v: unknown) => {
                                            const n = Number(v);
                                            return n > 0 ? `${selectedCurrency} ${n.toFixed(2)}` : '';
                                        }) as never}
                                    />
                                    <LabelList
                                        dataKey="percentage"
                                        position="top"
                                        fill="#2a2520"
                                        style={{ fontSize: 12, fontWeight: 700 }}
                                        formatter={((v: unknown) => {
                                            const n = Number(v);
                                            return n > 0 ? `${n.toFixed(1)}%` : '';
                                        }) as never}
                                    />
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </>
            ) : (
                <div className="text-center py-5 text-secondary">
                    <i className="bi bi-bar-chart display-4 d-block mb-3 opacity-25"></i>
                    <p className="fs-5 fw-medium mb-1">No expenses this period</p>
                    <small>Try a different month or currency</small>
                </div>
            )}
        </div>
    );
};

export default GroupDetailsTotals;