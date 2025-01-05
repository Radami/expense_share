import Login from "./Login";
import Logout from "./Logout";
import Profile from "./Profile";

function NavbarProfile({ loginParams }) {

    return (
        <li className="nav-item dropdown">
            <a className="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false">
            { 
                loginParams.isAuthenticated ? ( 
                    <>Profile</>
                ) : (
                    <>Login</>
                )
            }
            </a>
            <ul className="dropdown-menu" aria-labelledby="navbarDropdown">
                <li className="mx-3">
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