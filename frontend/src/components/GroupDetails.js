import axios from 'axios';
import React, { useEffect, useState } from 'react';
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
    const [group, setGroup] = useState({ group_members: [] });

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
                setGroup(response.data);
            } catch (error) {
              console.error('Error fetching profile', error);
            }
        };
      
        fetchGroupDetails();
        }, [loginParams.token, group_id]);

    return (
        <div className="container col-lg-4 mt-3 text-white">
        {loginParams.isAuthenticated ? (
        <>
            <span className="h1">{group["name"]} - </span><span className="h2">{group["description"]}</span>
            
            <Tabs
                defaultActiveKey="members"
                id="fill-tab-example"
                className="mb-3 custom-tab-margin"
                variant='pills'
            >
                <Tab eventKey="expenses" title="Expenses">
                    <GroupDetailsExpenses group_expenses={group["expenses"]} group_members={group["group_members"]} group_id={group_id} loginParams={loginParams}/>
                </Tab>
                <Tab eventKey="members" title="Members">
                    <GroupDetailsMembers group_members={group["group_members"]} group_id={group_id} loginParams={loginParams} />
                </Tab>
                <Tab eventKey="totals" title="Totals">
                    <GroupDetailsTotals groupTotals={group["totals"]} groupId={group_id} loginParams={loginParams} />
                </Tab>
                <Tab eventKey="balances" title="Balances">
                    <GroupDetailsBalances groupBalances={group["balances"]} groupMembers={group["group_members"]} groupId={group_id} loginParams={loginParams}/>
                </Tab>
            </Tabs>    
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