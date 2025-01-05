import axios from 'axios';
import React, { useState } from 'react';

const Login = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        axios.post('http://localhost:8000/users/api/token/', {
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
            <div className="my-1">
                <label htmlFor="loginEmailInput">Username</label>
                <input className="form-control" type="text" id="loginEmailInput" value={username} onChange={(e) => setUsername(e.target.value)} />
            </div> 
            <div className="my-1">
                <label htmlFor="loginPasswordInput">Password</label>
                <input className="form-control" type="password" id="loginPasswordInput" value={password} onChange={(e) => setPassword(e.target.value)} />
            </div>
            <button className="btn btn-primary my-1" type="submit">Login</button>
        </form>
    );
};

export default Login;
