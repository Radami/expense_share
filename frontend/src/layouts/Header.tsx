import { NavLink } from "react-router-dom";
import logo from '../../public/assets/logo-compressed.png';

const NAV_LINKS = [
    { label: "Groups",  to: "/",            end: true  },
    { label: "Friends", to: "/friends",     end: false },
    { label: "Profile", to: "/auth/profile", end: false },
];

const Header: React.FC = () => {
    return (
        <header className="sticky-top bg-color py-2">
            <div className="container col-lg-6">
                <nav className="navbar splittime-nav bg-white border rounded-4 shadow-sm py-0 px-3">
                    <NavLink className="navbar-brand d-flex align-items-center gap-2 fw-bold py-2 text-dark text-decoration-none" to="/">
                        <img src={logo} alt="Splittime logo" width="28" height="28" />
                        Splittime
                    </NavLink>
                    <ul className="navbar-nav flex-row gap-1 mb-0">
                        {NAV_LINKS.map(({ label, to, end }) => (
                            <li key={to} className="nav-item">
                                <NavLink
                                    className={({ isActive }) => `nav-link px-3 py-2${isActive ? ' active' : ''}`}
                                    to={to}
                                    end={end}
                                >
                                    {label}
                                </NavLink>
                            </li>
                        ))}
                    </ul>
                </nav>
            </div>
        </header>
    );
};

export default Header;