import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import {
    useParams
} from "react-router-dom";
import GroupDetailsBalances from './GroupDetailsBalances';
import GroupDetailsExpenses from './GroupDetailsExpenses';
import GroupDetailsMembers from './GroupDetailsMembers';
import GroupDetailsTotals from './GroupDetailsTotals';

function GroupDetails({ loginParams}) {

    const { group_id } = useParams();
    const [isAddExpenseModalOpen, setIsAddExpenseModalOpen] = React.useState(false);
    const [isAddMemberModalOpen, setIsAddMemberModalOpen] = React.useState(false);

    const [groupName, setGroupName] = useState("");
    const [groupDescription, setGroupDescription] = useState("");
    const [groupExpenses, setGroupExpenses] = useState([]);
    const [groupMembers, setGroupMembers] = useState([]);
    const [groupTotals, setGroupTotals] = useState([]);
    const [groupBalances, setGroupBalances] = useState([]);

    useEffect(() => {
        const fetchGroupDetails = async () => {
            const token = localStorage.getItem('access_token');
            
            try {
                
                const response = await axios.get('http://localhost:8000/splittime/api/group_details',
                {
                    params: {group_id},
                    headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                    }
                });
                setGroupName(response.data.name);
                setGroupDescription(response.data.groupDescription)
                setGroupExpenses(response.data.expenses);
                setGroupMembers(response.data.group_members);
                setGroupTotals(response.data.totals);
                setGroupBalances(response.data.balances)

            } catch (error) {
              console.error('Error fetching profile', error);
            }
        };
      
        fetchGroupDetails();
        }, [loginParams.token, group_id]);

    const handleAddExpenseModalOpen = () => {
        setIsAddExpenseModalOpen(true);
    };

    const handleAddExpenseModalClose = () => {
        setIsAddExpenseModalOpen(false);
    }

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
                    const updatedExpenses = [...groupExpenses, response.data];
                    setGroupExpenses(updatedExpenses);
                    //setHeaders(processMonthHeaders(updatedExpenses));
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

        handleAddExpenseModalClose();
    }

    const handleAddMemberModalOpen = () => {
        setIsAddMemberModalOpen(true);
    };

    const handleAddMemberModalClose = () => {
        setIsAddMemberModalOpen(false);
    }

    return (
        <div className="container col-lg-4 mt-3">
        {loginParams.isAuthenticated ? (
        <>
            <div>
                <div className="d-flex justify-content-between align-items-center">
                    <span className="h1">{groupName}</span>
                
                <div className="d-flex justify-content-end">
                    <button className="btn btn-success h-75 me-2" type="submit" onClick={handleAddExpenseModalOpen}><i className="bi bi-cash-stack" /><span className="ms-1">Add Expense</span></button>
                    <button className="btn btn-success h-75" type="submit" onClick={handleAddMemberModalOpen}><i className="bi bi-person-plus-fill" /><span className="ms-1">Add Member</span></button>
                </div>
                </div>
            </div>
            
            <Tabs
                defaultActiveKey="expenses"
                id="fill-tab-example"
                className="mb-3 custom-tab-margin"
                variant='pills'
            >
                <Tab eventKey="expenses" title="Expenses">
                    <GroupDetailsExpenses group_expenses={groupExpenses} group_members={groupMembers} group_id={group_id} loginParams={loginParams}/>
                </Tab>
                <Tab eventKey="members" title="Members">
                    <GroupDetailsMembers group_members={groupMembers} group_id={group_id} loginParams={loginParams} />
                </Tab>
                <Tab eventKey="totals" title="Totals">
                    <GroupDetailsTotals groupTotals={groupTotals} groupId={group_id} loginParams={loginParams} />
                </Tab>
                
                <Tab eventKey="balances" title="Balances">
                    <GroupDetailsBalances groupBalances={groupBalances} groupMembers={groupMembers} groupId={group_id} loginParams={loginParams}/>
                </Tab>
            </Tabs>

            <Modal 
                show={isAddExpenseModalOpen}
                onHide={handleAddExpenseModalClose}
                dialogClassName="my-modal">
                <Modal.Header className="bg-color2 border-0 ">
                    <Modal.Title>Add Expense</Modal.Title>
                </Modal.Header>
                <Modal.Body className="bg-color2 px-0 pt-0">
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
                                            {groupMembers.map((m) => (
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
                                    <button className="btn btn-secondary" onClick={handleAddExpenseModalClose}><span className="ms-1">Close</span></button>
                                </div>
                                <div className="d-flex">
                                    <button className="btn btn-success" type="submit"><i className="bi bi-person-plus-fill" /><span className="ms-1">Add Expense</span></button>
                                </div>
                            </div>
                        </div>
                    </form>
                    
                </Modal.Body>
            </Modal>
        </>
        ): (
            <p>
                Please log in
            </p>
        )
        }
        </div>
    );
}

export default GroupDetails;