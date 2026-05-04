import { useNavigate } from "react-router";
import type { GroupType } from '../../src/Types';

interface GroupProps {
    group: GroupType,
}

const Group: React.FC<GroupProps> = ({ group }) => {
    const navigate = useNavigate();

    const isOwedPill = group.user_is_owed === "Nothing"
        ? <span className="badge rounded-pill bg-body-secondary text-secondary fw-medium px-3 py-2">You are owed nothing</span>
        : <span className="badge rounded-pill bg-success-subtle text-success-emphasis fw-semibold px-3 py-2">You are owed {group.user_is_owed}</span>;

    const owesPill = group.user_owes === "Nothing"
        ? <span className="badge rounded-pill bg-body-secondary text-secondary fw-medium px-3 py-2">You owe nothing</span>
        : <span className="badge rounded-pill bg-danger-subtle text-danger-emphasis fw-semibold px-3 py-2">You owe {group.user_owes}</span>;

    return (
        <div
            className="card border shadow-sm rounded-3 group-card-hover"
            onClick={() => navigate(`/group/${group.id}`)}
        >
            <div className="card-body p-3">
                <div className="d-flex align-items-center">
                    <div className="flex-grow-1 pe-3">
                        <h5 className="fw-bold mb-1 text-dark">{group.name}</h5>
                        {group.description && <p className="text-secondary small mb-2">{group.description}</p>}
                        <div className="d-flex flex-wrap gap-2">
                            {isOwedPill}
                            {owesPill}
                        </div>
                    </div>
                    <div className="d-flex align-items-center gap-1 flex-shrink-0">
                        <span className="group-card-open-label text-secondary small fw-medium">Open</span>
                        <i className="bi bi-chevron-right text-secondary small"></i>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Group;