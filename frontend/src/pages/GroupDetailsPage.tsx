import { useEffect, useState } from 'react';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import { useNavigate } from "react-router-dom";
import {
    useParams
} from "react-router-dom";
import { type BalancesType, type ExpenseType, type GroupMemberType } from '../Types';
import api from '../utils/axios';
import GroupDetailsBalances from './GroupDetailsBalances';
import GroupDetailsExpenses from './GroupDetailsExpenses';
import GroupDetailsMembers from './GroupDetailsMembers';
import GroupDetailsTotals from './GroupDetailsTotals';


interface GroupDetailsProps {
}

export default function GroupDetailPage() {

    // "" is used to make the type "string" instead of "string | undefined"
    const { group_id = "" } = useParams<string>();

    // TODO: Remove isAuth
    const [isAuth, setIsAuth] = useState(false);

    // TODO: implement dedicated requests for each component
    const [groupName, setGroupName] = useState("");
    const [groupDescription, setGroupDescription] = useState("");
    const [groupExpenses, setGroupExpenses] = useState<ExpenseType[]>([]);
    const [groupMembers, setGroupMembers] = useState<GroupMemberType[]>([]);
    const [groupTotals, setGroupTotals] = useState<Record<string, number>>({});
    const [groupBalances, setGroupBalances] = useState<BalancesType>({});

    const navigate = useNavigate();

    useEffect(() => {
        const fetchGroupDetails = async () => {
            
            try {
                
                const response = await api.get('http://localhost:8000/splittime/api/group_details',
                {
                    params: {group_id},
                });
                setGroupName(response.data.name);
                setGroupDescription(response.data.groupDescription)
                setGroupExpenses(response.data.expenses);
                setGroupMembers(response.data.group_members);
                setGroupTotals(response.data.totals);
                setGroupBalances(response.data.balances);
                setIsAuth(true);

            } catch (error) {
                console.error('Error fetching profile', error);
                setIsAuth(false);
            }
        };
      
        fetchGroupDetails();
    }, [group_id]);

    return (
        <div>
        {isAuth ? (
        <>
            <div>
                <div className="d-flex justify-content-between align-items-center">
                    <span className="h1">{groupName}</span>
                
                <div className="d-flex justify-content-end">
                    <button className="btn btn-success h-75 me-2" type="button" onClick={() => navigate('/add_expense/' + group_id)}><i className="bi bi-cash-stack" /><span className="ms-1">Add Expense</span></button>
                    <button className="btn btn-success h-75" type="submit"><i className="bi bi-person-plus-fill" /><span className="ms-1">Add Member</span></button>
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
                    <GroupDetailsExpenses group_expenses={groupExpenses} group_members={groupMembers} group_id={group_id} />
                </Tab>
                <Tab eventKey="members" title="Members">
                    <GroupDetailsMembers group_members={groupMembers} group_id={group_id} />
                </Tab>
                <Tab eventKey="totals" title="Totals">
                    <GroupDetailsTotals groupTotals={groupTotals} />
                </Tab>
                
                <Tab eventKey="balances" title="Balances">
                    <GroupDetailsBalances group_balances={groupBalances} group_members={groupMembers} group_id={group_id} />
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
