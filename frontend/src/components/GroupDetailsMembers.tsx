import axios from 'axios';
import { useEffect, useState } from 'react';

import { GroupMember, loginParamsType } from '../Types';

interface GroupDetailsMembersProps {
    group_members: GroupMember[],
    group_id: number,
    loginParams: loginParamsType

}

const GroupDetailsMembers: React.FC<GroupDetailsMembersProps> = ({ group_members, group_id, loginParams }) => {

    const [members, setMembers] = useState(group_members)

      // Update state when the prop changes
    useEffect(() => {
        setMembers(group_members);
    }, [group_members]); // This will trigger whenever initialValue changes

    const deleteGroupMember = (group_member_id: number) => {
        axios.post('http://localhost:8000/splittime/api/delete_group_member',
        {
            user_id : group_member_id,
            group_id : group_id
        },
        {
            headers: {
            'Authorization': `Bearer ${loginParams.token}`,
            'Content-Type': 'application/json',
            }
        }).then(response => {
            if (response.status === 200) {
                console.log("Delete Group Member Success");
                const updatedGroupMembers = members.filter(group_member => group_member.id !== group_member_id)
                setMembers(updatedGroupMembers)
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
        
    };

    function addGroup(e : React.FormEvent<HTMLFormElement>) { // e is typed as a form event
        e.preventDefault(); // Prevent form from reloading the page
        const formData = new FormData(e.target as HTMLFormElement); // Use e.target to get the form
        const member_email = formData.get("member_email");

        axios.post('http://localhost:8000/splittime/api/add_group_member',
            {
                member_email : member_email,
                group_id : group_id
            },
            {
                headers: {
                'Authorization': `Bearer ${loginParams.token}`,
                'Content-Type': 'application/json',
                }
            }
        ).then(response => {
            if (response.status === 201) {
                console.log("Add Group Member Success", response.data);
                const updatedGroupMembers = [...members, response.data]
                setMembers(updatedGroupMembers)
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
        
      }

    return (
        <div>
            {members && members.length > 0 ? 
                members.map((gm) => (
                <div key={gm.id}>
                    <div className="d-flex justify-content-between">
                        <div className='d-flex justify-content-start'>
                            <div className="">
                                <i className="bi bi-person-fill fs-1" />
                            </div>
                            
                            <div className="container">
                                <div className="row"> 
                                    <span className="fs-4">{gm.username}</span>
                                </div>
                                <div className="row"> 
                                    <span className="fs-6">{gm.email}</span>
                                </div>
                            </div>
                        </div>
                        <div className="col-1 d-flex justify-content-center">
                            <button className="btn-red-circle" onClick={() => {deleteGroupMember(gm.id)}}>
                                <i className="bi bi-x-circle-fill"></i>
                            </button>
                        </div>
                    </div>
                </div>
            )): (<p>No members found</p>)}
            <div className="container mt-3">
            <form onSubmit={addGroup}>
                <div className="d-flex justify-content-center">   
                    <div>
                        <div className="input-group">
                            <span className="input-group-text">email</span>
                            <input className="form-control" placeholder="Enter user's email" type="text" id="member_email" name="member_email" />
                        </div>
                    </div>
                    <button className="btn btn-success mx-2" type="submit"><i className="bi bi-person-plus-fill" /><span className="ms-1">Add User</span></button>
                </div>
            </form>
            </div>
        </div>
    );
}

export default GroupDetailsMembers;