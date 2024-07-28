import logo from '../assets/logo-compressed.png';
import NavbarProfile from './navbar_profile';

function Header ({loginParams}) {
    return (
        <header>
          <div className="container d-flex col-lg-4 mt-3 ">
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark w-100">
                <div className="container-fluid">
                    <a className="navbar-brand fs-2 align-text-center text-white" href="#">
                        <img className="d-inline-block" src={logo} alt="Logo" width="48" height="48" />
                        <span>Splittime</span>
                    </a>
                    <ul className="navbar-nav d-flex flex-row fs-4">
                        <li className="nav-item mx-1">
                            <a className="nav-link text-white" aria-current="page" href="#">Groups</a>
                        </li>
                        <li className="nav-item mx-1">
                            <a className="nav-link text-white" aria-current="page" href="#">Friends</a>
                        </li>
                        <NavbarProfile loginParams={loginParams}/>
                    </ul>                    
                </div>  
            </nav>
          </div>
        </header>
    );
}

export default Header;