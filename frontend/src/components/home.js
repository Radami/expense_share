import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import Group from './group';

const Home = ({ loginParams }) => {

    const [groups, setGroups] = useState([]);
    const [open, setOpen] = React.useState(false);
    const [groupName, setGroupName] = useState('');
    const [groupDescription, setGroupDescription] = useState('');
 
    const handleClose = () => {
        setOpen(false);
    };
 
    const handleOpen = () => {
        setOpen(true);
    };

    useEffect(() => {
        const fetchGroups = async () => {
            const token = localStorage.getItem('access_token');
            try {
              const response = await axios.get('http://localhost:8000/splittime/api/group_index', {
                headers: {
                  'Authorization': `Bearer ${token}`
                }
              });
              setGroups(response.data);
            } catch (error) {
              console.error('Error fetching profile', error);
            }
          };
      
          fetchGroups();
        }, [loginParams.token]);

    const addGroup = () => {
            try {
                const response = axios.post('http://localhost:8000/splittime/api/add_group', 
                {
                    name: groupName,
                    description: groupDescription,
                },
                {
                  headers: {
                    'Authorization': `Bearer ${loginParams.token}`,
                    'Content-Type': 'application/json',
                  }
                });
                setGroups(response.data);
            } catch (error) {
                console.error('Error fetching profile', error);
            }
            handleClose();
        }

    return (
        <>
            <div className="container col-lg-4 mt-3 text-white">
            {loginParams.isAuthenticated ? (
                <>
                    {groups.map((group) => (
                        <Group key={group.id} group={group} />
                    ))}
                    <div className="container d-flex justify-content-center mt-3">
                        <button className="btn btn-success d-flex align-items-center" onClick={handleOpen}>
                            <i className="bi bi-people-fill"></i>
                            <span>Add Group</span>
                        </button>
                    </div>
                    <Modal 
                        show={open}
                        onHide={handleClose}>
                        <Modal.Header className="bg-color2 text-white border-0">
                            <Modal.Title>Add Group</Modal.Title>
                        </Modal.Header>
                        <Modal.Body className="bg-color2 text-white">
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
                        </Modal.Body>
                        <Modal.Footer className="bg-color2 border-0 text-white">
                        <Button variant="secondary" onClick={handleClose}>
                            Close
                        </Button>
                        <Button className="btn-success" onClick={addGroup}>
                            Save Changes
                        </Button>
                        </Modal.Footer>
                    </Modal>
                </>    
            ) : (
                <p>
                    Please log in
                </p>
            )
            }
            </div>
        </>
   );
}

export default Home;