import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Modal from 'react-bootstrap/Modal';

function GroupDetailsExpenses({group_expenses, group_members, group_id, loginParams}) {

    const [expenses, setExpenses] = useState(group_expenses)
    const [open, setOpen] = React.useState(false);

    // Update state when the prop changes
    useEffect(() => {
        setExpenses(group_expenses)
    }, [group_expenses]); // This will trigger whenever initialValue changes

    const handleClose = () => {
        setOpen(false);
    };
 
    const handleOpen = () => {
        setOpen(true);
    };

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

        handleClose();
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
            <div>
                <button className="btn btn-success col-2" type="submit" onClick={handleOpen}><i className="bi bi-person-plus-fill" /><span className="ms-1">Add Expense</span></button>
            </div>
            <Modal 
                show={open}
                onHide={handleClose}
                dialogClassName="my-modal">
                <Modal.Header className="bg-color2 text-white border-0 ">
                    <Modal.Title>Add Expense</Modal.Title>
                </Modal.Header>
                <Modal.Body className="bg-color2 text-white px-0 pt-0">
                    <form className="d-flex justify-content-center align-items-center" onSubmit={addExpense}>
                        <div className="col px-3">
                            <div className="row p-1">   
                                <div className="input-group">
                                    <span className="input-group-text">name</span>
                                    <input className="form-control" placeholder="Enter expense name" type="text" id="name" name="name" />
                                </div>
                            </div>
                            <div className="row p-1"> 
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
                            </div>
                            <div className="row p-1"> 
                                <div className="input-group">
                                        <span className="input-group-text">amount</span>
                                        <input className="form-control" placeholder="Amount" type="text" id="amount" name="amount" />
                                        
                                            <select id="currency" 
                                                    className="form-select form-select-md"
                                                    name="currency"
                                                    style={{  
                                                        minWidth: 0, // Allow shrinking below Bootstrap's default min-width from .form-select
                                                        flex: '0 0 auto', // Prevent flexbox from forcing size to expand to fill available space
                                                        width: 'auto', // Adjust width to content 
                                                    }}
                                            >
                                                <option value="USD">USD</option>
                                                <option value="YEN">YEN</option>
                                                <option value="EUR">EUR</option>
                                                <option value="GBP">GBP</option>
                                            </select>                                 
                                        
                                </div>
                            </div>
                            <div className="d-flex justify-content-end p-1 mt-3"> 
                                <div className="d-flex mx-2">
                                    <button className="btn btn-secondary" onClick={handleClose}><span className="ms-1">Close</span></button>
                                </div>
                                <div className="d-flex">
                                    <button className="btn btn-success" type="submit"><i className="bi bi-person-plus-fill" /><span className="ms-1">Add Expense</span></button>
                                </div>
                            </div>
                        </div>
                    </form>
                    
                </Modal.Body>
            </Modal>
            <div className="container mt-3">
                
            </div>
        </div>
    );
}

export default GroupDetailsExpenses;