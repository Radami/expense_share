import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true, // This is crucial for sending cookies
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a response interceptor
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If the error is 401 and we haven't tried to refresh the token yet
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                // Try to refresh the token
                await api.post('/users/api/token/refresh/');
                
                // Retry the original request
                return api(originalRequest);
            } catch (refreshError) {
                // If refresh fails, redirect to login
                window.location.href = '/auth/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default api; 