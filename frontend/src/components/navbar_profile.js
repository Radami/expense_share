import Login from "./login";
import Logout from "./logout";
import Profile from "./profile";

function NavbarProfile({ loginParams }) {

    return (
        <li className="nav-item dropdown">
            <a className="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            { 
                loginParams.isAuthenticated ? ( 
                    <>Profile</>
                ) : (
                    <>Login</>
                )
            }
            </a>
            <ul className="dropdown-menu" aria-labelledby="navbarDropdown">
                <li className="dropdown-item">
                { 
                    loginParams.isAuthenticated ? ( 
                    <>
                        <Profile token={loginParams.token}/>
                        <Logout onLogout={ loginParams.handleLogout }/>
                    </>
                    ) : (
                    <>
                        <Login onLogin={loginParams.handleLogin}/>
                    </>
                    )
                }  
                </li>
            </ul>
        </li>

    );
}

export default NavbarProfile;