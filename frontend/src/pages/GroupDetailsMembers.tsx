import { useEffect, useState } from 'react';
import { type GroupMemberType } from '../Types';
import api from '../utils/axios';
import { getAvatarBgClass } from '../utils/avatar';

interface GroupDetailsMembersProps {
    group_members: GroupMemberType[],
    group_id: string,
}


const GroupDetailsMembers: React.FC<GroupDetailsMembersProps> = ({ group_members, group_id }) => {
    const [members, setMembers] = useState(group_members);

    useEffect(() => {
        setMembers(group_members);
    }, [group_members]);

    const deleteGroupMember = (id: number) => {
        api.post('http://localhost:8000/splittime/api/delete_group_member', { user_id: id, group_id })
            .then(response => {
                if (response.status === 200) {
                    setMembers(ms => ms.filter(m => m.id !== id));
                }
            })
            .catch(error => console.error('Error deleting member', error));
    };

    function addGroupMember(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const member_email = new FormData(form).get('member_email');
        api.post('http://localhost:8000/splittime/api/add_group_member', { member_email, group_id })
            .then(response => {
                if (response.status === 201) {
                    setMembers(ms => [...ms, response.data]);
                    form.reset();
                }
            })
            .catch(error => console.error('Error adding member', error));
    }

    return (
        <div>
            <div className="d-flex flex-column gap-2 mb-3">
                {members && members.length > 0 ? members.map(m => (
                    <div key={m.id} className="card border shadow-sm rounded-3">
                        <div className="card-body p-3">
                            <div className="d-flex align-items-center gap-3">
                                <div className={`avatar-md rounded-circle text-white d-flex align-items-center justify-content-center fw-bold flex-shrink-0 ${getAvatarBgClass(m.username)}`}>
                                    {m.username.slice(0, 2).toUpperCase()}
                                </div>
                                <div className="flex-grow-1">
                                    <div className="fw-bold text-dark small">{m.username}</div>
                                    <div className="text-secondary" style={{ fontSize: '0.75rem' }}>{m.email}</div>
                                </div>
                                <button
                                    className="btn btn-link text-secondary p-2 rounded-2 delete-btn-hover flex-shrink-0"
                                    onClick={() => deleteGroupMember(m.id)}
                                    title="Remove member"
                                >
                                    <i className="bi bi-x-lg"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                )) : (
                    <div className="text-center py-5 text-secondary">
                        <i className="bi bi-people display-4 d-block mb-3 opacity-25"></i>
                        <p className="fs-5 fw-medium mb-1">No members yet</p>
                        <small>Add someone below to get started</small>
                    </div>
                )}
            </div>

            <div className="card card-dashed rounded-3">
                <div className="card-body p-3">
                    <form onSubmit={addGroupMember} className="d-flex align-items-center gap-3">
                        <div className="flex-grow-1">
                            <label htmlFor="member_email" className="member-form-label text-uppercase fw-bold d-block mb-1">
                                Email
                            </label>
                            <input
                                className="form-control border-0 bg-transparent shadow-none p-0"
                                type="email"
                                id="member_email"
                                name="member_email"
                                placeholder="friend@example.com"
                            />
                        </div>
                        <button className="btn btn-success btn-sm d-flex align-items-center gap-2 flex-shrink-0" type="submit">
                            <i className="bi bi-person-plus"></i> Add
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default GroupDetailsMembers;
