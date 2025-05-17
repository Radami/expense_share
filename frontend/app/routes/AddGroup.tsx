import axios from 'axios';
import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import type { LoginParamsType } from '../Types';



interface AddGroupProps {
    login_params: LoginParamsType
}

const AddGroup: React.FC<AddGroupProps> = ({ login_params }) => {

    const [groupName, setGroupName] = useState('');
    const [groupDescription, setGroupDescription] = useState('');

    const addGroup = () => {
        axios.post('http://localhost:8000/splittime/api/add_group', 
            {
                name: groupName,
                description: groupDescription,
            },
            {
                headers: {
                'Authorization': `Bearer ${login_params.token}`,
                'Content-Type': 'application/json',
                }
            }).then(response => {
                if (response.status === 201) {
                    console.log("Add success", response.data)
                }
            }).catch(error => {
                // Something happened in setting up the request that triggered an Error
                console.log('Error', error.message);
            })
    }

    return (
        <>
            <Form>
                <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
                <Form.Label>Name</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Name"
                    onChange={(e) => setGroupName(e.target.value)}
                    autoFocus
                />
                </Form.Group>
                <Form.Group
                    className="mb-3"
                    controlId="exampleForm.ControlTextarea1">
                    <Form.Label>Description</Form.Label>
                    <Form.Control 
                        type="text"
                        placeholder="Description" 
                        onChange={(e) => setGroupDescription(e.target.value)}
                    />
                </Form.Group> 
            </Form>
            <button className="secondary" onClick={handleClose}>
                Close
            </button>
            <button className="btn-success" onClick={addGroup}>
                Save Changes
            </button>
        </>
    )
}

export default AddGroup;