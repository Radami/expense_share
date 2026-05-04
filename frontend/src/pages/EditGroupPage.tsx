import { useEffect, useState } from 'react';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';
import api from '../utils/axios';

export default function EditGroupPage() {
    const { group_id } = useParams<{ group_id: string }>();
    const [searchParams] = useSearchParams();
    const returnTab = searchParams.get('return_tab') ?? 'expenses';
    const navigate = useNavigate();

    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [minimizeBalances, setMinimizeBalances] = useState(false);
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchGroup = async () => {
            try {
                const response = await api.get('/splittime/api/group_details', {
                    params: { group_id },
                });
                setName(response.data.name);
                setDescription(response.data.description);
                setMinimizeBalances(response.data.minimize_balances_setting);
            } catch (err) {
                console.error('Error fetching group', err);
                setError('Could not load group details');
            } finally {
                setIsLoading(false);
            }
        };
        fetchGroup();
    }, [group_id]);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError('');
        try {
            await api.post('/splittime/api/update_group_settings', {
                group_id: group_id,
                name: name,
                description: description,
                minimize_balances_setting: minimizeBalances,
            });
            navigate(`/group/${group_id}?tab=${returnTab}`);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to save changes');
        }
    };

    const handleDelete = async () => {
        try {
            await api.post('/splittime/api/delete_group', { id: group_id });
            navigate('/');
        } catch (err: any) {
            setError(err.response?.data || 'Failed to delete group');
        }
    };

    if (isLoading) {
        return (
            <div className="d-flex justify-content-center py-5">
                <div className="spinner-border text-success" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    }

    return (
        <div className="py-4">
            <div style={{ maxWidth: 600, margin: '0 auto' }}>
                <div className="mb-4">
                    <h1 className="fw-bold mb-1">Edit Group</h1>
                    <p className="text-secondary small mb-0">Update group details and settings</p>
                </div>

                <div className="card border shadow-sm rounded-3 mb-3">
                    <div className="card-body p-4">
                        {error && <div className="alert alert-danger small py-2">{error}</div>}
                        <form onSubmit={handleSubmit} id="edit-group-form">
                            <div className="mb-3">
                                <label htmlFor="groupName" className="member-form-label text-uppercase fw-bold d-block mb-1">
                                    Group name
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="groupName"
                                    value={name}
                                    onChange={e => setName(e.target.value)}
                                    required
                                />
                            </div>

                            <div className="mb-4">
                                <label htmlFor="groupDescription" className="member-form-label text-uppercase fw-bold d-block mb-1">
                                    Description
                                </label>
                                <input
                                    type="text"
                                    className="form-control"
                                    id="groupDescription"
                                    value={description}
                                    onChange={e => setDescription(e.target.value)}
                                />
                            </div>

                            <div className="mb-4">
                                <label className="member-form-label text-uppercase fw-bold d-block mb-2">
                                    Settings
                                </label>
                                <div className="form-check form-switch">
                                    <input
                                        className="form-check-input"
                                        type="checkbox"
                                        id="minimizeBalancesToggle"
                                        checked={minimizeBalances}
                                        onChange={e => setMinimizeBalances(e.target.checked)}
                                    />
                                    <label className="form-check-label small fw-medium text-secondary" htmlFor="minimizeBalancesToggle">
                                        Minimize balances
                                    </label>
                                </div>
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
                                    <i className="bi bi-check-lg"></i> Save changes
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

                <div className="card border border-danger-subtle shadow-sm rounded-3">
                    <div className="card-body p-4">
                        <h6 className="fw-bold text-danger mb-1">Danger zone</h6>
                        <p className="text-secondary small mb-3">Permanently delete this group and all its expenses. This cannot be undone.</p>
                        <button
                            className="btn btn-outline-danger btn-sm d-flex align-items-center gap-2"
                            type="button"
                            onClick={handleDelete}
                        >
                            <i className="bi bi-trash3"></i> Delete group
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}