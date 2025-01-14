import axios from 'axios';
import { AnimatePresence, motion } from 'framer-motion';
import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import { GroupType, LoginParamsType } from '../Types';
import Group from './Group';


interface HomeProps {
    login_params: LoginParamsType
}

const Home: React.FC<HomeProps> = ({ login_params }) => {

    const [groups, setGroups] = useState<GroupType[]>([]);
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
        }, [login_params.token]);

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
                    const updatedGroups = [...groups, response.data]
                    setGroups(updatedGroups);
                }
            }).catch(error => {
                // Something happened in setting up the request that triggered an Error
                console.log('Error', error.message);
            })
            
       
        handleClose();
    }

    const deleteGroup = (group_id: string) => {
        axios.post('http://localhost:8000/splittime/api/delete_group', 
            {
                id: group_id,
            },
            {
                headers: {
                'Authorization': `Bearer ${login_params.token}`,
                'Content-Type': 'application/json',
                }
            }).then(response=> {
                if (response.status === 200) {
                    console.log('Delete Group Success:', response.data);
                    const updatedGroups = groups.filter(group => group.id !== group_id)
                    setGroups(updatedGroups)
                } else if (response.status === 404) {
                    console.log('Not found');
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
            })
    }

    return (
        <>
            <div className="container col-lg-4 mt-3 text-dark">
            {login_params.isAuthenticated ? (
                <>
                    <AnimatePresence>
                        {groups.map((group) => (
                            <motion.div
                            key={group.id}
                            layout
                            initial={{ opacity: 0, y: -50 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            transition={{
                                opacity: { duration: 0.3 },
                                layout: { duration: 0.3 },
                                scale: { duration: 0.2 }
                              }}>
                                <Group key={group.id} 
                                   group={group}
                                   delete_function={() => deleteGroup(group.id)} />
                            </motion.div>
                        ))}

                         <motion.div
                            key="add_group_button"
                            layout
                            transition={{ 
                                opacity: { duration: 0.3 },
                                layout: { duration: 0.3 },
                                scale: { duration: 0.2 }
                            }}>    
                            <div className="container d-flex justify-content-center mt-3">
                                <button className="btn btn-success d-flex align-items-center" onClick={handleOpen}>
                                    <i className="bi bi-people-fill"></i>
                                    <span>Add Group</span>
                                </button>
                            </div>
                        </motion.div>   
                    </AnimatePresence>
                
                    <Modal 
                        show={open}
                        onHide={handleClose}>
                        <Modal.Header className="bg-color2 border-0">
                            <Modal.Title>Add Group</Modal.Title>
                        </Modal.Header>
                        <Modal.Body className="bg-color2">
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