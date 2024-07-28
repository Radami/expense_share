import axios from 'axios';
import React, { useState } from 'react';

const Login = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        axios.post('http://localhost:8000/api/token/', {
            username,
            password,
        })
        .then(response => {
            const access_token = response.data.access;
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            axios.defaults.headers['Authorization'] = 'Bearer ' + response.data.access;
            onLogin(access_token);
        })
        .catch(error => {
            // TODO: handle error requests when logging in           
            console.error(error);
        });
    };

    return (
        <form onSubmit={handleLogin} >
        <div>
            <label>Username</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div>
            <label>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <button type="submit">Login</button>
        </form>
    );
};

export default Login;
