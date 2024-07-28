import axios from 'axios';

function Logout({ onLogout }) {

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        axios.defaults.headers['Authorization'] = '';
        onLogout();
    }

    return (
        <form onSubmit={handleLogout} className="text-white">
          <button type="submit">Logout</button>
        </form>
      );
}

export default Logout;