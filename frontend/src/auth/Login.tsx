import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import api from '../utils/axios';
import type * as Route from "./+types.Login";

export default function Login({actionData}: Route.ComponentProps) {
    const [error, setError] = useState("");
    const navigate = useNavigate();
    const [isHydrated, setIsHydrated] = useState(false);
    const [searchParams] = useSearchParams();

    useEffect(() => {
        setIsHydrated(true);
    }, []);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const username = formData.get("username")?.toString();
        const password = formData.get("password")?.toString();
        
        if (!username || !password) {
            setError("Username and password are required");
            return;
        }
        
        try {
            const response = await api.post('/users/api/token/', {
                username,
                password
            });

            console.log("Login successful:", response);
            const redirectTo = searchParams.get("redirectTo") || "/";
            navigate(redirectTo);
        } catch (err: any) {
            setError(err.response?.data?.detail || "Login failed");
        }
    }

    return (
        <form onSubmit={handleSubmit} >
            <div className="my-1">
                <label htmlFor="loginEmailInput">Username</label>
                <input className="form-control" type="text" id="loginUserNameInput" name="username" />
            </div> 
            <div className="my-1">
                <label htmlFor="loginPasswordInput">Password</label>
                <input className="form-control" type="password" id="loginPasswordInput" name="password" />
            </div>
            {isHydrated && error && <div className="text-danger my-1">{error}</div>}
            <button className="btn btn-primary my-1" type="submit">Login</button>
        </form>
    );
}