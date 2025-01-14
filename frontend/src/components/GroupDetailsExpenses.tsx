import axios from 'axios';
import React, { useEffect, useState } from 'react';

import { ExpenseType, GroupMemberType, LoginParamsType } from '../Types';

interface GroupDetailsExpensesProps {
    group_expenses: ExpenseType[],
    group_members: GroupMemberType[],
    group_id: string,
    loginParams: LoginParamsType,
}

const GroupDetailsExpenses: React.FC<GroupDetailsExpensesProps> = ({group_expenses, group_members, group_id, loginParams}) => {

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


        axios.post('http://localhost:8000/splittime/api/delete_group_expense',
            {
                expense_id: id
            },
            {
                headers: {
                'Authorization': `Bearer ${loginParams.token}`,
                'Content-Type': 'application/json',
                }
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
        <div className="container px-0">
            {expenses && expenses.length > 0 ? 
                expenses.map((e, index) => (
                <React.Fragment key={e.id}>
                    { headers[index] && (
                        <div className="mt-3 fw-bold text-color6">
                            {headers[index]}
                        </div>
                    )}
                    <div key={e.id} className={`container ${index !== expenses.length - 1 ? 'border-bottom' : ''} border-color1`}>
                        <div className="row">
                            <div className="col-6 d-flex align-items-center">
                                <div className="d-flex flex-column align-items-center justify-content-start">
                                    <span className="fs-6">
                                        { getDayFromDate(e.creation_date) }
                                    </span>
                                </div>
                            
                                <div className="ps-3">
                                    <span className="fs-5">
                                        {e.name}
                                    </span>
                                </div>
                            </div>
                            
                            <div className="col-6 d-flex justify-content-end align-items-center">
                                <div className="d-flex flex-column align-items-center me-3">
                                    <div>
                                        <span className="me-1">
                                            {e.payee}
                                        </span>                             
                                    </div>
                                    <div>
                                    <span className="fs-8">
                                        { e.amount } {e.currency}
                                    </span>
                                    </div>
                                </div>

                                <div className="d-flex flex-column align-items-center me-3">
                                    <div>
                                        <span>You are owned</span>
                                    </div>
                                    <div>
                                        <span>100 USD</span>
                                    </div>
                                </div>

                                <div className="d-flex">
                                    <div className="d-flex justify-content-end">
                                        <button className="btn-red-circle" onClick={() => {deleteExpense(e.id)}}>
                                            <i className="bi bi-x-circle-fill"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </React.Fragment>   
            )): (<p>No expenses found</p>)}
        </div>
    );
}

export default GroupDetailsExpenses;