import React, { useEffect, useState } from 'react';
import { type ExpenseType, type GroupMemberType } from '../Types';
import api from '../utils/axios';

interface GroupDetailsExpensesProps {
    group_expenses: ExpenseType[],
    group_members: GroupMemberType[],
    group_id: string,
}

const GroupDetailsExpenses: React.FC<GroupDetailsExpensesProps> = ({group_expenses, group_members, group_id }) => {

    const [expenses, setExpenses] = useState(group_expenses);
    const [open, setOpen] = useState(false);
    const [headers, setHeaders] = useState<Record<number, string>>({});

    // Update state when the prop changes
    useEffect(() => {
        setExpenses(group_expenses)
        setHeaders(processMonthHeaders(expenses));
    }, [group_expenses]); // This will trigger whenever initialValue changes

    function processMonthHeaders(expenses: ExpenseType[]) : Record<number, string> {
        if (!expenses || expenses.length === 0)
            return {};
        let headersMapping: Record<number, string> = {};
        headersMapping[0] = getMonthAndYearFromDate(expenses[0].creation_date);
        for (let i = 1;i < expenses.length; i++) {
            if (getMonthFromDate(expenses[i].creation_date) !==
                getMonthFromDate(expenses[i-1].creation_date)) 
                {
                    headersMapping[i] = getMonthAndYearFromDate(expenses[i].creation_date);
            }
        }
        return headersMapping;
    }
    
    function deleteExpense(id: string) {
        api.post('http://localhost:8000/splittime/api/delete_group_expense',
            {
                expense_id: id
            }).then(response => {
                if (response.status === 200) {
                    console.log("Delete expense success", response.data);
                    const updatedExpenses = expenses.filter(expense => expense.id !== id)
                    setExpenses(updatedExpenses)
                    setHeaders(processMonthHeaders(updatedExpenses));
                }
            }).catch(error => {
                if (error.response) {
                    // The request was made and the server responded with a status code
                    // that falls out of the range of 2xx
                    console.log('Error status code:', error.response.status);
                } else if (error.request) {
                    // The request was made but no response was received
                    console.log('No response received:', error.request);
                } else {
                    // Something happened in setting up the request that triggered an Error
                    console.log('Error', error.message);
                }
            });
    }

    function getMonthAndYearFromDate(datetime: string) {
        var dt = new Date(datetime);
        return getMonthFromDate(datetime) + 
               " " + 
               dt.getUTCFullYear();
    }

    function getMonthFromDate(datetime: string) {
        const monthNames = ["January",
                            "February",
                            "March",
                            "April",
                            "May",
                            "June",
                            "July",
                            "August",
                            "September",
                            "October",
                            "November",
                            "December"];
        var dt = new Date(datetime);
        return monthNames[dt.getUTCMonth()];
    }

    function getDayFromDate(datetime: string) {
        var dt = new Date(datetime);
        return dt.getUTCDate();
    }

    return (
        <div className="container-fluid px-0">
            {expenses && expenses.length > 0 ? 
                expenses.map((e, index) => (
                <React.Fragment key={e.id}>
                    { headers[index] && (
                        <div className="d-flex align-items-center py-2 my-3 border-bottom border-2 border-light">
                            <div className="d-flex align-items-center text-secondary fw-semibold text-uppercase letter-spacing-1">
                                <i className="bi bi-calendar-event me-2"></i>
                                {headers[index]}
                            </div>
                        </div>
                    )}
                    <div key={e.id} className="card border-light shadow-sm mb-2 expense-card-hover">
                        <div className="card-body p-2">
                            <div className="row align-items-center">
                                <div className="col-auto">
                                    <div className="date-circle d-flex align-items-center justify-content-center rounded-4 bg-gradient-primary text-white fw-semibold">
                                        <span className="fs-6">{ getDayFromDate(e.creation_date) }</span>
                                    </div>
                                </div>
                                
                                <div className="col">
                                    <div className="d-flex flex-column gap-2">
                                        <div>
                                            <h6 className="mb-0 fw-semibold text-dark">{e.name}</h6>
                                        </div>
                                        
                                        <div className="d-flex flex-wrap gap-3 align-items-center">
                                            <div className="d-flex align-items-center gap-2">
                                                <span className="text-muted small fw-medium">Paid by:</span>
                                                <span className="text-secondary fw-semibold small">{e.payee}</span>
                                            </div>
                                            
                                            <div className="d-flex align-items-center">
                                                <span className="badge bg-success-subtle text-success fw-bold px-3 py-2 rounded-pill">
                                                    { e.amount } {e.currency}
                                                </span>
                                            </div>
                                            
                                            <div className="d-flex align-items-center gap-2">
                                                <span className="text-muted small fw-medium">You owe:</span>
                                                <span className="badge bg-danger-subtle text-danger fw-semibold px-3 py-2 rounded-pill">
                                                    100 USD
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div className="col-auto">
                                    <button 
                                        className="btn btn-link text-muted p-2 rounded-3 delete-btn-hover" 
                                        onClick={() => {deleteExpense(e.id)}}
                                        title="Delete expense"
                                    >
                                        <i className="bi bi-trash3 fs-6"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </React.Fragment>   
            )): (
                <div className="text-center py-5 text-muted">
                    <i className="bi bi-receipt-cutoff display-4 text-light mb-3 d-block"></i>
                    <p className="fs-5 fw-medium mb-1">No expenses found</p>
                    <small className="text-muted">Add your first expense to get started</small>
                </div>
            )}
        </div>
    );
}

export default GroupDetailsExpenses;