// src/components/Profile.js
import axios from 'axios';
import React, { useEffect, useState } from 'react';

const Profile = ({ token }) => {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
        const token = localStorage.getItem('access_token');
        try {
          const response = await axios.get('http://localhost:8000/users/api/profile/', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          setProfile(response.data);
        } catch (error) {
          console.error('Error fetching profile', error);
        }
      };
  
      fetchProfile();
    }, [token]);

  return (
    <div>
      {profile ? (
        <div>
          <h2>{profile.username}</h2>
          <p>Email: {profile.email}</p>
        </div>
      ) : (
        <p>Please log in</p>
      )}
    </div>
  );
};

export default Profile;
