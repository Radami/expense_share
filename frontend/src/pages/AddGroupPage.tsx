import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../utils/axios';

export default function AddGroupPage() {
    const [groupName, setGroupName] = useState('');
    const [description, setDescription] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError('');

        try {
            const response = await api.post('/splittime/api/add_group', {
                name: groupName,
                description: description
            });

            if (response.status === 201) {
                navigate('/');
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to create group');
        }
    };

    return (
        <div>
            <h2>Create New Group</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="groupName" className="form-label">Group Name</label>
                    <input
                        type="text"
                        className="form-control"
                        id="groupName"
                        value={groupName}
                        onChange={(e) => setGroupName(e.target.value)}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="description" className="form-label">Description</label>
                    <textarea
                        className="form-control"
                        id="description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        rows={3}
                    />
                </div>
                {error && <div className="alert alert-danger">{error}</div>}
                <button type="submit" className="btn btn-primary">Create Group</button>
            </form>
        </div>
    );
} 