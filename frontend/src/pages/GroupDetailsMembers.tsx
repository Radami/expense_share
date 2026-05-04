import { useEffect, useState } from 'react';
import { type GroupMemberType } from '../Types';
import { getAvatarBgClass } from '../utils/avatar';
import api from '../utils/axios';

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
        api.post('/splittime/api/delete_group_member', { user_id: id, group_id })
            .then(response => {
                if (response.status === 200) {
                    setMembers(ms => ms.filter(m => m.id !== id));
                }
            })
            .catch(error => console.error('Error deleting member', error));
    };

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
                        <small>Use "Add member" to invite someone</small>
                    </div>
                )}
            </div>
        </div>
    );
};

export default GroupDetailsMembers;
