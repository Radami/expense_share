import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { useNavigate, type MetaFunction } from "react-router";
import Group from '../components/Group';
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
    const [isLoading, setIsLoading] = useState(true);
    const [isError, setIsError] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchGroups = async () => {
            try {
                const response = await api.get('/splittime/api/group_index');
                setGroups(response.data);
            } catch (error) {
                console.error('Error fetching groups', error);
                setIsError(true);
            } finally {
                setIsLoading(false);
            }
        };

        fetchGroups();
    }, []);

    return (
        <>
            <div className="py-4">
                {isLoading ? (
                    <div className="d-flex justify-content-center py-5">
                        <div className="spinner-border text-success" role="status">
                            <span className="visually-hidden">Loading...</span>
                        </div>
                    </div>
                ) : isError ? (
                    <div className="text-center py-5 text-secondary">
                        <i className="bi bi-exclamation-circle display-4 d-block mb-3 opacity-50"></i>
                        <p className="fs-5 fw-medium mb-1">Something went wrong</p>
                        <small>Please try again later</small>
                    </div>
                ) : (
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
                )}
            </div>
        </>
    );
}
