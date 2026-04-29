import React, { useEffect, useState } from 'react';
import type { ExpenseType, GroupMemberType } from '../Types';

interface GroupDetailsTotalsProps {
    groupExpenses: ExpenseType[],
    groupMembers: GroupMemberType[]
}

const GroupDetailsTotals: React.FC<GroupDetailsTotalsProps> = ({ groupExpenses, groupMembers }) => {
    
    const [expenses, setExpenses] = useState(groupExpenses)
    const [totals, setGroupMembers] = useState(groupMembers)
    

    const months = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']

    const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth())
    const [selectedYear, setSelectedYear] = useState(new Date().getFullYear())
    const [selectedCurrency, setSelectedCurrency] = useState('');

    useEffect(() => {
        setExpenses(groupExpenses)
        setGroupMembers(groupMembers)
    }, [groupMembers]); // This will trigger whenever initialValue changes

    function getCurrencies(): Array<string> {
        if (expenses.length == 0)
            return ["No expenses"]
        return [...new Set(expenses.map(expense => expense.currency))];
    }

    function getTotalExpenseByDate(): number {
        return expenses.filter(expense => expense.currency == selectedCurrency)
                       .filter(expense => { 
                            const d = new Date(expense.creation_date);
                            return d.getMonth() === selectedMonth && d.getFullYear() === selectedYear
                        })
                        .reduce((sum,expense) => sum + expense.amount, 0);
    }

    return (
        <div>
            <div className="d-flex gap-5">
                <div className="d-flex">
                    <select 
                        id="currencySelect"
                        className="form-select" 
                        value={selectedCurrency}
                        onChange={(e) => setSelectedCurrency(e.target.value)}
                    >
                            {getCurrencies().map(currency => (
                        <option key={currency} value={currency}>{currency}</option>
                    ))}
                    </select>
                </div>
                <div className="d-flex" id="monthYearHeading">
                    <div className="d-flex">
                        <button className="btn btn-sm btn-outline-secondary m-1" id="prevYear" onClick={() => {selectedMonth == 0 ? setSelectedMonth(11) : setSelectedMonth(selectedMonth-1)}}>&lt;</button>
                        <h5 className="mt-2 month-heading" id="currentYear">{months[selectedMonth]}</h5>
                        <button className="btn btn-sm btn-outline-secondary m-1" id="nextYear" onClick={() => {selectedMonth == 11 ? setSelectedMonth(0) : setSelectedMonth(selectedMonth+1)}}>&gt;</button>
                    </div>
                    <div className="d-flex">
                        <button className="btn btn-sm btn-outline-secondary m-1" id="prevYear" onClick={() => {setSelectedYear(selectedYear-1)}}>&lt;</button>
                        <h5 className="mt-2" id="currentYear">{selectedYear}</h5>
                        <button className="btn btn-sm btn-outline-secondary m-1" id="nextYear" onClick={() => {setSelectedYear(selectedYear+1)}}>&gt;</button>
                    </div>
                </div>
            </div>
            <div>
                <div className="card shadow-sm">
                    <div className="card-body">
                        <h5 className="card-title mb-4">
                            <i className="bi bi-receipt-cutoff me-2"></i>
                            {getTotalExpenseByDate()}
                        </h5>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default GroupDetailsTotals;