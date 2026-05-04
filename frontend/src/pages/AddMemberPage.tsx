import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../utils/axios';

export default function AddMemberPage() {
    const { group_id } = useParams<{ group_id: string }>();
    const [error, setError] = useState<string>('');
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError('');
        const formData = new FormData(e.currentTarget);
        try {
            const response = await api.post('/splittime/api/add_group_member', {
                member_email: formData.get('member_email'),
                group_id,
            });
            if (response.status === 201) {
                navigate(`/group/${group_id}`);
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to add member');
        }
    };

    return (
        <div className="py-4">
            <div style={{ maxWidth: 600, margin: '0 auto' }}>
                <div className="mb-4">
                    <h1 className="fw-bold mb-1">Add Member</h1>
                    <p className="text-secondary small mb-0">Invite someone to join this group by email</p>
                </div>

                <div className="card border shadow-sm rounded-3">
                    <div className="card-body p-4">
                        {error && <div className="alert alert-danger small py-2">{error}</div>}
                        <form onSubmit={handleSubmit}>
                            <div className="mb-4">
                                <label htmlFor="member_email" className="member-form-label text-uppercase fw-bold d-block mb-1">Email address</label>
                                <input
                                    type="email"
                                    className="form-control"
                                    id="member_email"
                                    name="member_email"
                                    placeholder="friend@example.com"
                                    required
                                />
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
                                    <i className="bi bi-person-plus"></i> Add member
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}
