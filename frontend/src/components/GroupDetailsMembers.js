import React from 'react';

function GroupDetailsMembers({ group_members }) {

    return (
        <div className="container">
            {group_members && group_members.length > 0 ? 
                group_members.map((gm) => (
                <div key={gm.id} className="container">
                    <div className="row">
                        <div className="col-1">
                            <i className="bi bi-person-fill fs-1" />
                        </div>
                        
                        <div className="col-4">
                            <div className="row"> 
                                <span className="fs-4">{gm.username}</span>
                            </div>
                            <div className="row"> 
                                <span className="fs-6">{gm.email}</span>
                            </div>
                        </div>
                        
                        <div className="col-1">
                            <button className="btn-red-circle">
                                <i className="bi bi-x-circle-fill"></i>
                            </button>
                        </div>
                    </div>
                </div>
            )): (<p>No members found</p>)}
        </div>
    );
}

export default GroupDetailsMembers;