import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { Link, useNavigate, type MetaFunction } from "react-router";
import Group from '../components/Group';
import type { GroupType, LoginParamsType } from '../Types';
import api from '../utils/axios';
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

export default function HomePage({ loaderData }: Route.ComponentProps) {
    const [groups, setGroups] = useState<GroupType[]>([]);

    // TODO: remove isAuth
    const [isAuth, setIsAuth] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchGroups = async () => {
            try {
                const response = await api.get('/splittime/api/group_index');
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
        api.post('/splittime/api/delete_group', 
            {
                id: group_id,
            }
        ).then(response => {
            if (response.status === 200) {
                console.log('Delete Group Success:', response.data);
                const updatedGroups = groups.filter(group => group.id !== group_id)
                setGroups(updatedGroups)
            } else if (response.status === 404) {
                console.log('Not found');
            }
        }).catch(error => {
            if (error.response) {
                console.log('Error status code:', error.response.status);
            } else if (error.request) {
                console.log('No response received:', error.request);
            } else {
                console.log('Error', error.message);
            }
        });
    }

    return (
        <>
            <div className="text-dark">
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
                                    <Group 
                                        key={group.id} 
                                        group={group}
                                        delete_function={() => deleteGroup(group.id)} 
                                    />
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
                                    <button 
                                        className="btn btn-success d-flex align-items-center" 
                                        onClick={() => navigate('/add_group')}
                                    >
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
                )}
            </div>
        </>
    );
}
