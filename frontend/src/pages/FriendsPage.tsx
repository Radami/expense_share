import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { FriendGroupEntry, FriendType } from '../Types';
import { getAvatarBgClass } from '../utils/avatar';
import api from '../utils/axios';

// ── FriendGroupRow ───────────────────────────────────────────────────────────

function FriendGroupRow({ group, onNavigate }: { group: FriendGroupEntry; onNavigate: (id: number) => void }) {
    const hasOwed = group.owed_to.length > 0;
    const hasOwe = group.you_owe.length > 0;
    const settled = !hasOwed && !hasOwe;

    return (
        <button
            type="button"
            className="friend-group-row d-flex align-items-center gap-3 w-100 text-start rounded-3 px-3 py-2"
            onClick={() => onNavigate(group.id)}
        >
            <div
                className={`rounded-circle flex-shrink-0 ${settled ? 'bg-secondary' : hasOwed ? 'bg-success' : 'bg-danger'}`}
                style={{ width: 8, height: 8 }}
            />
            <span className="fw-semibold small flex-grow-1 text-truncate text-dark">{group.name}</span>
            <div className="d-flex gap-2 flex-shrink-0 align-items-center">
                {hasOwed || hasOwe ? (
                    <>
                        {group.owed_to.map((o, i) => (
                            <span key={i} className="badge rounded-pill bg-success-subtle text-success-emphasis fw-semibold px-2 py-1">
                                +{o.currency} {o.amount.toFixed(2)}
                            </span>
                        ))}
                        {group.you_owe.map((o, i) => (
                            <span key={i} className="badge rounded-pill bg-danger-subtle text-danger-emphasis fw-semibold px-2 py-1">
                                −{o.currency} {o.amount.toFixed(2)}
                            </span>
                        ))}
                    </>
                ) : (
                    <span className="badge rounded-pill bg-body-secondary text-secondary fw-semibold px-2 py-1">Settled</span>
                )}
            </div>
            <i className="bi bi-chevron-right text-secondary flex-shrink-0" style={{ fontSize: '0.6875rem' }} />
        </button>
    );
}

// ── FriendCard ───────────────────────────────────────────────────────────────

function FriendCard({ friend, defaultOpen = false, onNavigate }: {
    friend: FriendType;
    defaultOpen?: boolean;
    onNavigate: (id: number) => void;
}) {
    const [open, setOpen] = useState(defaultOpen);

    const totalOwed = friend.net.filter(n => n.amount > 0);
    const totalOwe  = friend.net.filter(n => n.amount < 0);

    return (
        <div className={`card border shadow-sm rounded-3 overflow-hidden ${!open ? 'group-card-hover' : ''}`}>
            {/* Clickable header */}
            <div
                className="d-flex align-items-center gap-3 px-4 py-3"
                onClick={() => setOpen(o => !o)}
                style={{ cursor: 'pointer' }}
            >
                <div
                    className={`rounded-circle text-white d-flex align-items-center justify-content-center fw-bold flex-shrink-0 ${getAvatarBgClass(friend.username)}`}
                    style={{ width: 44, height: 44, fontSize: '0.9375rem', letterSpacing: '-0.02em' }}
                >
                    {friend.username.slice(0, 2).toUpperCase()}
                </div>

                <div className="flex-grow-1 overflow-hidden">
                    <div className="d-flex align-items-baseline gap-2 mb-1">
                        <span className="fw-bold" style={{ textTransform: 'capitalize' }}>{friend.username}</span>
                        <span className="text-secondary text-truncate" style={{ fontSize: '0.75rem' }}>{friend.email}</span>
                    </div>
                    <div className="d-flex gap-2 flex-wrap">
                        {totalOwed.length > 0 || totalOwe.length > 0 ? (
                            <>
                                {totalOwed.map((n, i) => (
                                    <span key={i} className="badge rounded-pill bg-success-subtle text-success-emphasis fw-semibold px-2 py-1">
                                        Owes you {n.currency} {n.amount.toFixed(2)}
                                    </span>
                                ))}
                                {totalOwe.map((n, i) => (
                                    <span key={i} className="badge rounded-pill bg-danger-subtle text-danger-emphasis fw-semibold px-2 py-1">
                                        You owe {n.currency} {Math.abs(n.amount).toFixed(2)}
                                    </span>
                                ))}
                            </>
                        ) : (
                            <span className="badge rounded-pill bg-body-secondary text-secondary fw-semibold px-2 py-1">All settled</span>
                        )}
                    </div>
                </div>

                {/* Group count badge */}
                <div
                    className="d-flex flex-column align-items-center px-3 py-1 rounded-2 flex-shrink-0 bg-body-secondary"
                    style={{ minWidth: 52 }}
                >
                    <span className="fw-bold lh-1" style={{ fontSize: '1.0625rem' }}>
                        {friend.groups.length}
                    </span>
                    <span
                        className="text-uppercase fw-semibold"
                        style={{ fontSize: '0.625rem', letterSpacing: '0.04em' }}
                    >
                        {friend.groups.length === 1 ? 'group' : 'groups'}
                    </span>
                </div>

                {/* Chevron */}
                <i
                    className="bi bi-chevron-right text-secondary flex-shrink-0"
                    style={{ transition: 'transform 0.2s', transform: open ? 'rotate(90deg)' : 'rotate(0deg)', fontSize: '0.875rem' }}
                />
            </div>

            {/* Expanded section */}
            {open && (
                <div className="border-top px-3 py-3" style={{ background: 'var(--bg)' }}>
                    <div className="member-form-label text-uppercase fw-bold mb-2 ps-1">Shared groups</div>
                    <div className="d-flex flex-column gap-2">
                        {friend.groups.map(g => (
                            <FriendGroupRow key={g.id} group={g} onNavigate={onNavigate} />
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

// ── FriendsPage ──────────────────────────────────────────────────────────────

export default function FriendsPage() {
    const [friends, setFriends] = useState<FriendType[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isError, setIsError] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        api.get('/splittime/api/friends')
            .then(res => setFriends(res.data))
            .catch(() => setIsError(true))
            .finally(() => setIsLoading(false));
    }, []);

    return (
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
                    <div className="mb-4">
                        <div>
                            <h1 className="fw-bold mb-0"><i className="bi bi-people me-1"></i>Friends</h1>
                        </div>
                    </div>

                    {friends.length > 0 ? (
                        <AnimatePresence>
                            <div className="d-flex flex-column gap-2">
                                {friends.map((friend, i) => (
                                    <motion.div
                                        key={friend.id}
                                        initial={{ opacity: 0, y: -16 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ opacity: { duration: 0.2 }, delay: i * 0.04 }}
                                    >
                                        <FriendCard
                                            friend={friend}
                                            defaultOpen={false}
                                            onNavigate={id => navigate(`/group/${id}`)}
                                        />
                                    </motion.div>
                                ))}
                            </div>
                        </AnimatePresence>
                    ) : (
                        <div className="text-center py-5 text-muted">
                            <i className="bi bi-people display-4 text-light mb-3 d-block"></i>
                            <p className="fs-5 fw-medium mb-1">No friends yet</p>
                            <small className="text-muted d-block">Join or create a group to get started</small>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}