function AddExpenseModal() {
    
    
    
    return (
        <Modal 
            show={open}
            onHide={handleClose}
            dialogClassName="my-modal">
            <Modal.Header className="bg-color2 border-0 ">
                <Modal.Title>Add Expense</Modal.Title>
            </Modal.Header>
            <Modal.Body className="bg-color2 px-0 pt-0">
                <form className="d-flex justify-content-center align-items-center" onSubmit={addExpense}>
                    <div className="col px-3">
                        <div className="row p-1">   
                            <div className="input-group">
                                <span className="input-group-text">name</span>
                                <input className="form-control" placeholder="Enter expense name" type="text" id="name" name="name" />
                            </div>
                        </div>
                        <div className="row p-1"> 
                            <div className="input-group">
                                <div className="input-group">
                                    <span className="input-group-text">payee</span>
                                    <select id="payee" className="form-select form-select-sm" name="payee">
                                        {group_members.map((m) => (
                                            <option key={m.id} value={m.id}>{m.username}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div className="row p-1"> 
                            <div className="input-group">
                                    <span className="input-group-text">amount</span>
                                    <input className="form-control" placeholder="Amount" type="text" id="amount" name="amount" />
                                    
                                        <select id="currency" 
                                                className="form-select form-select-md"
                                                name="currency"
                                                style={{  
                                                    minWidth: 0, // Allow shrinking below Bootstrap's default min-width from .form-select
                                                    flex: '0 0 auto', // Prevent flexbox from forcing size to expand to fill available space
                                                    width: 'auto', // Adjust width to content 
                                                }}
                                        >
                                            <option value="USD">USD</option>
                                            <option value="YEN">YEN</option>
                                            <option value="EUR">EUR</option>
                                            <option value="GBP">GBP</option>
                                        </select>                                 
                                    
                            </div>
                        </div>
                        <div className="d-flex justify-content-end p-1 mt-3"> 
                            <div className="d-flex mx-2">
                                <button className="btn btn-secondary" onClick={handleClose}><span className="ms-1">Close</span></button>
                            </div>
                            <div className="d-flex">
                                <button className="btn btn-success" type="submit"><i className="bi bi-person-plus-fill" /><span className="ms-1">Add Expense</span></button>
                            </div>
                        </div>
                    </div>
                </form>
                
            </Modal.Body>
        </Modal>
    );
}

export default AddExpenseModal;