import { useNavigate } from "react-router";
import type { GroupType } from '../../src/Types';

interface GroupProps {
    group : GroupType,
    deleteGroup: Function,
}

const Group: React.FC<GroupProps> = ({group, deleteGroup}) => {

    const navigate = useNavigate();

    function buildIsOwedString(user_is_owed:string){
        if (user_is_owed == "Nothing")
            return <span className="badge bg-body-secondary text-success fw-bold px-3 py-2 rounded-pill"> You are owed nothing!</span>
        else
            return ( <>
                        <span className="text-muted small fw-medium">You are owed:</span>
                        <span className="badge bg-success-subtle text-success fw-bold px-3 py-2 rounded-pill">{user_is_owed}</span>
                   </>
            )
    }

    function buildOwesString(user_owes:string){
        if (user_owes == "Nothing")
            return <span className="badge bg-body-secondary text-success fw-bold px-3 py-2 rounded-pill" > You owe nothing!</span>
        else
            return ( <>
                        <span className="text-muted small fw-medium">You owe:</span>
                                <span className="badge bg-danger-subtle text-danger fw-semibold px-3 py-2 rounded-pill">{user_owes}</span>
                   </>
            )
    }

    return (
        <>
        
        <div className="card border-light shadow-sm group-card-hover">
            <div className="card-body p-3 position-relative">
                <div className="d-flex align-items-center">
                    <div className="flex-grow-1 pe-5">
                        <h6 className="mb-1 fw-semibold text-dark">{group.name}</h6>
                        <div className="text-muted small">{group.description}</div>
                        <div className="d-flex flex-wrap gap-3 align-items-center mt-2">
                            <div className="d-flex align-items-center gap-2">
                                {buildIsOwedString(group.user_is_owed)}
                            </div>
                            <div className="d-flex align-items-center gap-2" >
                                {buildOwesString(group.user_owes)}
                            </div>
                        </div>
                    </div>
                    {/* Top-right Open button */}
                    <button 
                        className="btn btn-primary d-flex align-items-center gap-2 position-absolute top-0 end-0 pt-1 px-2 mt-2 me-2"
                        onClick={() => navigate(`/group/${group.id}`)}
                        title="Open group"
                    >
                        <i className="bi bi-chevron-right"></i>
                    </button>

                    {/* Bottom-right Delete button */}
                    <button 
                        className="btn btn-link text-muted p-2 rounded-3 delete-btn-hover position-absolute bottom-0 end-0 mb-2 me-2"
                        onClick={() => deleteGroup(group.id)}
                        title="Delete group"
                    >
                        <i className="bi bi-trash3 fs-6"></i>
                    </button>
                </div>
            </div>
        </div>
        </>
    );
}

export default Group;