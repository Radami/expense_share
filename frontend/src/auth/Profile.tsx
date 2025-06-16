// src/components/Profile.js
import { useEffect, useState } from 'react';
import { type ProfileType } from '../Types';
import api from '../utils/axios';

interface ProfileProps {}

const Profile: React.FC<ProfileProps> = () => {
    const [profile, setProfile] = useState<ProfileType>(null);

    const logout = async () => {
        try {
            await api.post('/users/api/token/invalidate');
            setProfile(null);
        } catch (error) {
            console.error('Error invalidating token', error);
        }
    };

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

    return (
        <div>
            {profile ? (
                <div>
                    <div className="row">
                        <div className="">
                            <h2>{profile.username}</h2>
                        </div>
                        <div className="">
                            <p>Email: {profile.email}</p>
                        </div>
                        <div className="">
                            <button className="btn btn-secondary" onClick={logout}>Logout</button>
                        </div>
                    </div>
                </div>
            ) : (
                <p>Please log in</p>
            )}
        </div>
    );
};

export default Profile;
