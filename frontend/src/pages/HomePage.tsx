import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { Link, useNavigate, type MetaFunction } from "react-router";
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
            <div className="container py-3">
                {isAuth ? (
                    <>
                        <div className="d-flex align-items-center py-2 mb-3 border-bottom border-2 border-light">
                            <div className="d-flex align-items-center text-secondary fw-semibold text-uppercase">
                                <i className="bi bi-people me-2"></i>
                                Your Groups
                            </div>
                            <div className="ms-auto">
                                <button 
                                    className="btn btn-success d-flex align-items-center gap-2"
                                    onClick={() => navigate('/add_group')}
                                >
                                    <i className="bi bi-plus-lg"></i>
                                    <span>New Group</span>
                                </button>
                            </div>
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
                                        <div className="card border-light shadow-sm group-card-hover">
                                            <div className="card-body p-3 position-relative">
                                                <div className="d-flex align-items-center">
                                                    <div className="flex-grow-1 pe-5">
                                                        <h6 className="mb-1 fw-semibold text-dark">{group.name}</h6>
                                                        <div className="text-muted small">{group.description}</div>
                                                        <div className="d-flex flex-wrap gap-3 align-items-center mt-2">
                                                            <div className="d-flex align-items-center gap-2">
                                                                <span className="text-muted small fw-medium">You are owed:</span>
                                                                <span className="badge bg-success-subtle text-success fw-bold px-3 py-2 rounded-pill">0 USD</span>
                                                            </div>
                                                            <div className="d-flex align-items-center gap-2">
                                                                <span className="text-muted small fw-medium">You owe:</span>
                                                                <span className="badge bg-danger-subtle text-danger fw-semibold px-3 py-2 rounded-pill">0 USD</span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    {/* Top-right Open button */}
                                                    <button 
                                                        className="btn btn-primary d-flex align-items-center gap-2 position-absolute top-0 end-0 pt-1 px-2 mt-2 me-2"
                                                        onClick={() => navigate(`/group/${group.id}`)}
                                                        title="Open group"
                                                    >
                                                        <i className="bi bi-chevron-right"></i>
                                                    </button>

                                                    {/* Bottom-right Delete button */}
                                                    <button 
                                                        className="btn btn-link text-muted p-2 rounded-3 delete-btn-hover position-absolute bottom-0 end-0 mb-2 me-2"
                                                        onClick={() => deleteGroup(group.id)}
                                                        title="Delete group"
                                                    >
                                                        <i className="bi bi-trash3 fs-6"></i>
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
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
