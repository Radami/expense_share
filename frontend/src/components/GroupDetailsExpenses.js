import axios from 'axios';
import React, { useEffect, useState } from 'react';

function GroupDetailsExpenses({group_expenses, group_members, group_id, loginParams}) {

    const [expenses, setExpenses] = useState(group_expenses)

    // Update state when the prop changes
    useEffect(() => {
        setExpenses(group_expenses)
    }, [group_expenses]); // This will trigger whenever initialValue changes

    function addExpense(e) {
        e.preventDefault(); // Prevent form from reloading the page
        const formData = new FormData(e.target); // Use e.target to get the form
        const name = formData.get("name")
        const payee = formData.get("payee")
        const amount = formData.get("amount")
        const currency = formData.get("currency")

        console.log(formData)

        axios.post('http://localhost:8000/splittime/api/add_group_expense',
            {
                group_id: group_id,
                name: name,
                payee: payee,
                amount: amount,
                currency: currency
            },
            {
                headers: {
                'Authorization': `Bearer ${loginParams.token}`,
                'Content-Type': 'application/json',
                }
            }).then(response => {
                if (response.status === 201) {
                    console.log("Add expense success", response.data);
                    const updatedExpenses = [...expenses, response.data]
                    setExpenses(updatedExpenses)
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

    function deleteExpense(id) {


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

    function getMonthFromDate(datetime) {

        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        var dt = new Date(datetime);
        return monthNames[dt.getUTCMonth()];
    }

    function getDayFromDate(datetime) {
        var dt = new Date(datetime);
        return dt.getUTCDate();
    }

    return (
        <div className="container border border-1">
            {expenses && expenses.length > 0 ? 
                expenses.map((e) => (
                <div key={e.id} className="container border border-success">
                    <div className="row">
                        <div className="col-6 d-flex align-items-center">
                            <div className="d-flex flex-column align-items-center justify-content-start">
                                <span className="fs-4">
                                    { getDayFromDate(e.creation_date) }
                                </span>
                                   
                                <span className="fs-8">
                                    { getMonthFromDate(e.creation_date) }
                                </span>
                            </div>
                        
                            <div className="ps-3">
                                <span className="fs-3">
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
                                    <span>
                                        paid
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
            )): (<p>No expenses found</p>)}
        <div className="container mt-3">
            <form onSubmit={addExpense}>
                <div className="row">   
                    <div className="col-6">
                        <div className="input-group">
                                <span className="input-group-text">name</span>
                                <input className="form-control" placeholder="Enter expense name" type="text" id="name" name="name" />
                            </div>
                        </div>
                        <div className="input-group">
                            <div className="input-group">
                                <span className="input-group-text">payee</span>
                                <select id="payee" className="form-select form-select-sm" name="payee">
                                    {group_members.map((m) => (
                                        <option key={m.id} value={m.id}>{m.username}</option>
                                    ))}
                                </select>
                            </div>
                        </div>
                        <div className="input-group">
                            <div className="input-group">
                                <span className="input-group-text">amount</span>
                                <input className="form-control" placeholder="Enter amount" type="text" id="amount" name="amount" />
                                <select id="currency" className="form-select form-select-sm"  name="currency">
                                    <option value="USD">USD</option>
                                    <option value="YEN">YEN</option>
                                    <option value="EUR">EUR</option>
                                    <option value="GBP">GBP</option>
                                </select>
                            </div>
                        </div>
                        <div>
                            <button className="btn btn-success col-2" type="submit"><i className="bi bi-person-plus-fill" /><span className="ms-1">Add Expense</span></button>
                        </div>
                </div>
            </form>
            </div>
        </div>
    );
}

export default GroupDetailsExpenses;