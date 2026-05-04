import { useEffect, useState } from 'react';
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { type GroupMemberType, type GroupType } from '../Types';
import api from '../utils/axios';

export default function AddExpensePage() {
    const [groupMembers, setGroupMembers] = useState<GroupMemberType[]>([]);
    const [groups, setGroups] = useState<GroupType[]>([]);
    const [selectedGroupId, setSelectedGroupId] = useState<string>('');
    const [error, setError] = useState<string>('');
    const navigate = useNavigate();
    const { group_id: paramGroupId } = useParams<{ group_id: string }>();
    const [searchParams] = useSearchParams();
    const returnTab = searchParams.get('return_tab') ?? 'expenses';

    useEffect(() => {
        const fetchGroups = async () => {
            try {
                const response = await api.get('/splittime/api/group_index');
                setGroups(response.data);
                if (paramGroupId) {
                    setSelectedGroupId(paramGroupId);
                } else if (response.data.length > 0) {
                    setSelectedGroupId(response.data[0].id);
                }
            } catch (err) {
                console.error('Error fetching groups', err);
                setError('Failed to load groups');
            }
        };
        fetchGroups();
    }, [paramGroupId]);

    useEffect(() => {
        const fetchGroupDetails = async () => {
            if (!selectedGroupId) return;
            try {
                const response = await api.get('/splittime/api/group_details', {
                    params: { group_id: selectedGroupId },
                });
                setGroupMembers(response.data.group_members);
            } catch (err) {
                console.error('Error fetching group details', err);
                setError('Failed to load group members');
            }
        };
        fetchGroupDetails();
    }, [selectedGroupId]);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError('');
        const formData = new FormData(e.currentTarget);
        const expenseData = {
            group_id: selectedGroupId,
            name: formData.get('name'),
            payee: formData.get('payee'),
            amount: formData.get('amount'),
            currency: formData.get('currency'),
        };
        try {
            const response = await api.post('/splittime/api/add_group_expense', expenseData);
            if (response.status === 201) {
                navigate(`/group/${selectedGroupId}?tab=${returnTab}`);
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to add expense');
        }
    };

    return (
        <div className="py-4">
            <div style={{ maxWidth: 600, margin: '0 auto' }}>
                <div className="mb-4">
                    <h1 className="fw-bold mb-1">Add Expense</h1>
                    <p className="text-secondary small mb-0">Record a new shared expense for the selected group</p>
                </div>

                <div className="card border shadow-sm rounded-3">
                    <div className="card-body p-4">
                        {error && <div className="alert alert-danger small py-2">{error}</div>}
                        <form onSubmit={handleSubmit}>
                            <div className="mb-3">
                                <label htmlFor="group" className="member-form-label text-uppercase fw-bold d-block mb-1">Group</label>
                                <select
                                    id="group"
                                    className="form-select"
                                    value={selectedGroupId}
                                    onChange={e => setSelectedGroupId(e.target.value)}
                                >
                                    {groups.map(g => (
                                        <option key={g.id} value={g.id}>{g.name}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="mb-3">
                                <label htmlFor="name" className="member-form-label text-uppercase fw-bold d-block mb-1">Description</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="name"
                                    name="name"
                                    placeholder="e.g. Dinner at Mario's"
                                    required
                                />
                            </div>

                            <div className="d-flex gap-3 mb-3">
                                <div className="flex-grow-1">
                                    <label htmlFor="amount" className="member-form-label text-uppercase fw-bold d-block mb-1">Amount</label>
                                    <input
                                        type="number"
                                        className="form-control"
                                        id="amount"
                                        name="amount"
                                        placeholder="0.00"
                                        step="0.01"
                                        min="0"
                                        required
                                    />
                                </div>
                                <div style={{ width: 120 }}>
                                    <label htmlFor="currency" className="member-form-label text-uppercase fw-bold d-block mb-1">Currency</label>
                                    <select className="form-select" id="currency" name="currency">
                                        <option value="USD">USD</option>
                                        <option value="EUR">EUR</option>
                                        <option value="GBP">GBP</option>
                                        <option value="RON">RON</option>
                                        <option value="YEN">YEN</option>
                                    </select>
                                </div>
                            </div>

                            <div className="mb-4">
                                <label htmlFor="payee" className="member-form-label text-uppercase fw-bold d-block mb-1">Paid by</label>
                                <select className="form-select" id="payee" name="payee" required>
                                    {groupMembers.map(m => (
                                        <option key={m.id} value={m.id}>{m.username}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="d-flex justify-content-end gap-2">
                                <button
                                    className="btn btn-outline-secondary btn-sm"
                                    type="button"
                                    onClick={() => navigate(-1)}
                                >
                                    Cancel
                                </button>
                                <button className="btn btn-success btn-sm d-flex align-items-center gap-2" type="submit">
                                    <i className="bi bi-plus-lg"></i> Add expense
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}