import {
    Link
} from "react-router-dom";

function Group({group, deleteFunction}) {

    return (
        <div className="row p-1 bg-color2 border border-dark rounded">
            <div className="d-grid gap-2 col-md-10 mx-auto">
                <h3><Link to={`group/${group.id}`}>{ group.name }</Link></h3>
                <span>You are owed 100 USD</span>
                <span>User A owes you 100 USD</span>
            </div>
            <div className="d-grid gap-2 col-md-2 mx-auto">
                <button className="btn btn-primary d-flex align-items-center">
                    <i className="bi bi-plus-circle-fill me-1"></i>
                    <span>Expense</span>
                </button>
                <button className="btn btn-warning d-flex align-items-center">
                    <i className="bi bi-pencil-fill me-1"></i>
                    <span>Members</span>
                </button>
                <button className="btn btn-danger d-flex align-items-center" onClick={deleteFunction}>
                    <i className="bi bi-x-circle-fill me-1"></i>
                    <span>Group</span>
                </button>
            </div>
        </div>
    );
}

export default Group;