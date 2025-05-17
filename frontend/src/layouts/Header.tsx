import { Link } from "react-router-dom";
import logo from '../../public/assets/logo-compressed.png';

interface HeaderProps {

}

const Header: React.FC<HeaderProps> = () => {
    return (
        <header>
          <div>
            <nav className="navbar navbar-expand-lg w-100">
                <div className="container-fluid">
                    <a className="navbar-brand fs-2 align-text-center title-color1" href="/">
                        <img className="d-inline-block" src={logo} alt="Logo" width="48" height="48" />
                        <span>Splittime</span>
                    </a>
                    <ul className="navbar-nav d-flex flex-row fs-4">
                        <Link className="nav-link" to="/">Groups</Link>
                        <Link className="nav-link" to="/friends">Friends</Link>
                        <Link className="nav-link" to="/auth/profile">Profile</Link>
                    </ul>                    
                </div>  
            </nav>
          </div>
        </header>
    );
}

export default Header;