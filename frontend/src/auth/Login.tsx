import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import api from '../utils/axios';

export default function Login() {
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
    };

    return (
        <div className="py-4">
            <div style={{ maxWidth: 480, margin: '0 auto' }}>
                <div className="mb-4">
                    <h1 className="fw-bold mb-1">Sign in</h1>
                    <p className="text-secondary small mb-0">Enter your credentials to continue</p>
                </div>

                <div className="card border shadow-sm rounded-3">
                    <div className="card-body p-4">
                        {isHydrated && error && (
                            <div className="alert alert-danger small py-2">{error}</div>
                        )}
                        <form onSubmit={handleSubmit}>
                            <div className="mb-3">
                                <label htmlFor="loginUserNameInput" className="member-form-label text-uppercase fw-bold d-block mb-1">
                                    Username
                                </label>
                                <input
                                    className="form-control"
                                    type="text"
                                    id="loginUserNameInput"
                                    name="username"
                                    autoComplete="username"
                                />
                            </div>
                            <div className="mb-4">
                                <label htmlFor="loginPasswordInput" className="member-form-label text-uppercase fw-bold d-block mb-1">
                                    Password
                                </label>
                                <input
                                    className="form-control"
                                    type="password"
                                    id="loginPasswordInput"
                                    name="password"
                                    autoComplete="current-password"
                                />
                            </div>

                            <div className="d-flex justify-content-end">
                                <button className="btn btn-success btn-sm d-flex align-items-center gap-2" type="submit">
                                    <i className="bi bi-box-arrow-in-right"></i> Sign in
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}