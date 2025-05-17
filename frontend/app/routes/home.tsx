import axios from 'axios';
import { AnimatePresence, motion } from 'framer-motion';
import React, { useEffect, useState } from 'react';
import { Link, type MetaFunction } from "react-router";
import Group from '../components/Group';
import type { GroupType, LoginParamsType } from '../Types';
import type * as Route from "./+types.home";

interface HomeProps {
    login_params: LoginParamsType
}

export const meta: MetaFunction = () => {
    return [
      { title: "New React Router App" },
      { name: "description", content: "Welcome to React Router!" },
    ];
  };

export default function Index({ loaderData }: Route.ComponentProps) {

    const [groups, setGroups] = useState<GroupType[]>([]);
    const [open, setOpen] = React.useState(false);
    const [groupName, setGroupName] = useState('');
    const [groupDescription, setGroupDescription] = useState('');
    const [isAuth, setIsAuth] = useState(false);

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
                withCredentials: true
              });
              console.log("i am getting groups");
              setGroups(response.data);
              setIsAuth(true);
            } catch (error) {
              console.error('Error fetching groups', error);
                setIsAuth(false);
            }
        };

        fetchGroups();
        
        }, []);

    const deleteGroup = (group_id: string) => {
        axios.post('http://localhost:8000/splittime/api/delete_group', 
            {
                id: group_id,
            },
            {
                headers: {
                'Authorization': `Bearer ${loaderData.token}`,
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
            {isAuth ? (
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
                </>    
            ) : (
                <p>
                    <Link to="auth/login">Login</Link>
                </p>
            )
            }
            </div>
        </>
   );
}
