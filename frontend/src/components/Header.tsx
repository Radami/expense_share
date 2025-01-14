import { Link } from "react-router-dom";
import logo from '../assets/logo-compressed.png';
import { LoginParamsType } from '../Types';
import NavbarProfile from './NavbarProfile';

interface HeaderProps {
    loginParams: LoginParamsType,
}

const Header: React.FC<HeaderProps> = ({loginParams}) => {
    return (
        <header>
          <div className="container d-flex col-lg-4 mt-3 ">
            <nav className="navbar navbar-expand-lg w-100">
                <div className="container-fluid">
                    <a className="navbar-brand fs-2 align-text-center title-color1" href="#">
                        <img className="d-inline-block" src={logo} alt="Logo" width="48" height="48" />
                        <span>Splittime</span>
                    </a>
                    <ul className="navbar-nav d-flex flex-row fs-4">
                        <Link className="nav-link" to="/">Groups</Link>
                        <Link className="nav-link" to="/friends">Friends</Link>
                        <NavbarProfile loginParams={loginParams}/>
                    </ul>                    
                </div>  
            </nav>
          </div>
        </header>
    );
}

export default Header;