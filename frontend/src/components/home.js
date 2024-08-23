import axios from 'axios';
import React, { useEffect, useState } from 'react';
import Group from './group';

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
    <div className="container col-lg-4 mt-3 text-white">
        {loginParams.isAuthenticated ? ( 
            groups.map((group) => (
                <Group group={group} />
            ))    
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