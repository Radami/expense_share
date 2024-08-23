function Group({group}) {

    return (
        <div className="row p-1 bg-color2 border border-dark rounded">
            <div className="d-grid gap-2 col-md-10 mx-auto">
                <h3><a href="#">{ group.name }</a></h3>
                <span>You are owed 100 USD</span>
                <span>User A owes you 100 USD</span>
            </div>
            <div className="d-grid gap-2 col-md-2 mx-auto">
                <a className="btn btn-bd-test" href="#">Add Expense</a>
                <a className="btn btn-primary" href="#">Edit members</a>
                <a className="btn btn-outline-danger" href="#">Delete Group</a>
            </div>
        </div>
    );
}

export default Group;