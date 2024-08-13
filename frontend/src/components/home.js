import axios from 'axios';
import React, { useEffect, useState } from 'react';

const Home = ({ loginParams }) => {

    const [groups, setGroups] = useState([]);

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
        }, [loginParams.token]);

    return (
    <div className="text-white">
    {loginParams.isAuthenticated ? ( 
            <ul className="text-white">
            { groups.map((group) => (
                <li key={group.id}>{group.name}</li>
            ))}
            </ul>
        ) : (
        <p>
            Please log in
        </p>
        )
    }
    </div>
   );
}

export default Home;