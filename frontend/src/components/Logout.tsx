import axios from 'axios';

interface LogoutProps {
    onLogout: () => void;
}

const Logout: React.FC<LogoutProps> = ({ onLogout }) => {

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        axios.defaults.headers['Authorization'] = '';
        onLogout();
    }

    return (
        <form onSubmit={handleLogout} className="text-white">
          <button className="btn btn-secondary" type="submit">Logout</button>
        </form>
      );
}

export default Logout;