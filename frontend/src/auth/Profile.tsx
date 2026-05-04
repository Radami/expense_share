import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { type ProfileType } from '../Types';
import api from '../utils/axios';
import { getAvatarBgClass } from '../utils/avatar';

const Profile: React.FC = () => {
    const [profile, setProfile] = useState<ProfileType>(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await api.get('/users/api/profile/');
                setProfile(response.data);
            } catch (error) {
                console.error('Error fetching profile', error);
            }
        };

        fetchProfile();
    }, []);

    const handleLogout = async () => {
        try {
            await api.post('/users/api/token/invalidate');
            navigate('/auth/login');
        } catch (error) {
            console.error('Error invalidating token', error);
            navigate('/auth/login');
        }
    };

    if (!profile) {
        return (
            <div className="d-flex justify-content-center py-5">
                <div className="spinner-border text-success" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    }

    const initials = profile.username.slice(0, 2).toUpperCase();

    return (
        <div className="py-4">
            <div style={{ maxWidth: 420, margin: '0 auto' }}>
                <div className="mb-4">
                    <h1 className="fw-bold mb-1">Profile</h1>
                </div>

                <div className="card border shadow-sm rounded-3">
                    <div className="card-body p-4">
                        <div className="d-flex flex-column align-items-center text-center py-2 mb-4">
                            <div
                                className={`rounded-circle text-white d-flex align-items-center justify-content-center fw-bold mb-3 ${getAvatarBgClass(profile.username)}`}
                                style={{ width: 72, height: 72, fontSize: '1.5rem' }}
                            >
                                {initials}
                            </div>
                            <h5 className="fw-bold mb-1">{profile.username}</h5>
                            <span className="text-secondary small">{profile.email}</span>
                        </div>

                        <div className="d-flex justify-content-end">
                            <button
                                className="btn btn-outline-danger btn-sm d-flex align-items-center gap-2"
                                onClick={handleLogout}
                            >
                                <i className="bi bi-box-arrow-right"></i> Logout
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Profile;