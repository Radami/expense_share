import { useEffect, useState } from 'react';
import { useNavigate, useParams } from "react-router-dom";
import { type GroupMemberType, type GroupType } from '../Types';
import api from '../utils/axios';

export default function AddExpensePage() {
    const [groupMembers, setGroupMembers] = useState<GroupMemberType[]>([]);
    const [groups, setGroups] = useState<GroupType[]>([]);
    const [selectedGroupId, setSelectedGroupId] = useState<string>('');
    const [error, setError] = useState<string>('');
    const navigate = useNavigate();
    const { group_id: paramGroupId } = useParams<{ group_id: string }>();

    // Fetch all groups
    useEffect(() => {
        // When the component loads up for the first time, we fetch all groups.
        // We then check if we got a group id and select that group. Othertwise take the first one.
        // With that group, fetch all members.
        
        // TODO: handle empty cases
        
        const fetchGroups = async () => {
            try {
                const response = await api.get('/splittime/api/group_index');
                console.log("i am getting groups", response.data);
                setGroups(response.data);
                
                // If we have a group_id in the URL, select that group
                if (paramGroupId) {
                    setSelectedGroupId(paramGroupId);
                } else if (response.data.length > 0) {
                    // Otherwise select the first group
                    setSelectedGroupId(response.data[0].id);
                }
            } catch (error) {
                console.error('Error fetching groups', error);
                setError('Failed to load groups');
            }
        };

        fetchGroups();
    }, [paramGroupId]);

    // Fetch group members when selected group changes
    useEffect(() => {
        const fetchGroupDetails = async () => {
            if (!selectedGroupId) return;

            try {
                const response = await api.get('/splittime/api/group_details', {
                    params: { group_id: selectedGroupId }
                });
                setGroupMembers(response.data.group_members);


            } catch (error) {
                console.error('Error fetching group details', error);
                setError('Failed to load group members');
            }
        };

        fetchGroupDetails();
    }, [selectedGroupId]);

    const handleGroupChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedGroupId(e.target.value);
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError('');

        const formData = new FormData(e.currentTarget);
        const expenseData = {
            group_id: selectedGroupId,
            name: formData.get('name'),
            payee: formData.get('payee'),
            amount: formData.get('amount'),
            currency: formData.get('currency')
        };

        try {
            const response = await api.post('/splittime/api/add_group_expense', expenseData);
            if (response.status === 201) {
                // Navigate to the group details page
                navigate(`/group/${selectedGroupId}`);
            }
        } catch (error: any) {
            setError(error.response?.data?.detail || 'Failed to add expense');
        }
    };

    if (error) {
        return <div className="alert alert-danger">{error}</div>;
    }


    return (
        <>
            <h2>Add New Expense</h2>
            <form className="d-flex justify-content-center align-items-center" onSubmit={handleSubmit}>
                <div className="col px-3">
                    <div className="row p-1">   
                        <div className="input-group">
                        <label htmlFor="group" className="input-group-text">group</label>
                        <select 
                            id="group" 
                            className="form-select" 
                            value={selectedGroupId}
                            onChange={handleGroupChange}
                        >
                            {groups.map((group) => (
                                <option key={group.id} value={group.id}>
                                    {group.name}
                                </option>
                            ))}
                        </select>
                        </div>
                    </div>

                    <div className="row p-1"> 
                        <div className="input-group">
                            <label className="input-group-text">payee</label>
                            <select 
                                id="payee" 
                                className="form-select form-select-sm" 
                                name="payee"
                                required
                            >
                                {groupMembers.map((m) => (
                                    <option key={m.id} value={m.id}>
                                        {m.username}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <div className="row p-1">   
                        <div className="input-group">
                            <label className="input-group-text">name</label>
                            <input 
                                type="text" 
                                className="form-control" 
                                placeholder="Enter expense name" 
                                id="name" 
                                name="name" 
                                required
                            />
                        </div>
                    </div>

                    <div className="row p-1"> 
                        <div className="input-group">
                            <label className="input-group-text">amount</label>
                            <input 
                                type="number"
                                className="form-control" 
                                placeholder="Amount" 
                                id="amount" 
                                name="amount"
                                step="0.01"
                                required />
                            
                                <select 
                                    id="currency" 
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
                        <button className="btn btn-success" type="submit">
                            <i className="bi bi-person-plus-fill me-1" />
                            Add Expense
                        </button>
                        
                    </div>
                </div>
            </form>
    </>);
}