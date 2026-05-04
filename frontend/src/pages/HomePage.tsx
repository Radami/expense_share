import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { Link, useNavigate, type MetaFunction } from "react-router";
import Group from 'src/components/Group';
import type { GroupType } from '../Types';
import api from '../utils/axios';

// Intentionally no props; page fetches its own data

export const meta: MetaFunction = () => {
    return [
        { title: "New React Router App" },
        { name: "description", content: "Welcome to React Router!" },
    ];
};

export default function HomePage() {
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

    return (
        <>
            <div className="py-4">
                {isAuth ? (
                    <>
                        <div className="d-flex justify-content-between align-items-center mb-4">
                            <div>
                                <h1 className="fw-bold mb-0"><i className="bi bi-people me-1"></i>Your Groups</h1>
                            </div>
                            <button
                                className="btn btn-success d-flex align-items-center gap-2"
                                onClick={() => navigate('/add_group')}
                            >
                                <i className="bi bi-plus-lg"></i>
                                New Group
                            </button>
                        </div>

                        <AnimatePresence>
                            {groups && groups.length > 0 ? (
                                groups.map((group) => (
                                    <motion.div
                                        key={group.id}
                                        layout
                                        initial={{ opacity: 0, y: -20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0, scale: 0.95 }}
                                        transition={{
                                            opacity: { duration: 0.25 },
                                            layout: { duration: 0.25 },
                                            scale: { duration: 0.2 }
                                        }}
                                        className="mb-2"
                                    >
                                        <Group group={group} />
                                    </motion.div>
                                ))
                            ) : (
                                <div className="text-center py-5 text-muted">
                                    <i className="bi bi-people display-4 text-light mb-3 d-block"></i>
                                    <p className="fs-5 fw-medium mb-1">No groups yet</p>
                                    <small className="text-muted d-block mb-3">Create your first group to get started</small>
                                    <button 
                                        className="btn btn-success d-inline-flex align-items-center gap-2"
                                        onClick={() => navigate('/add_group')}
                                    >
                                        <i className="bi bi-plus-lg"></i>
                                        <span>Create Group</span>
                                    </button>
                                </div>
                            )}
                        </AnimatePresence>
                    </>
                ) : (
                    <div className="container d-flex justify-content-center mt-4">
                        <Link className="btn btn-outline-primary" to="auth/login">Login</Link>
                    </div>
                )}
            </div>
        </>
    );
}
