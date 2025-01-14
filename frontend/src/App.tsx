import { useEffect, useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import './App.css';
import Footer from './components/Footer';
import Friends from './components/Friends';
import GroupDetails from './components/GroupDetails';
import Header from './components/Header';
import Home from "./components/Home";
import { loginParamsType } from './Types';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [token, setToken] = useState<string>("");
    
    useEffect(() => {
        const storedToken : string = localStorage.getItem('access_token') ?? "";
        if (storedToken) {
            setIsAuthenticated(true);
            setToken(storedToken);
        }
        else {
            setIsAuthenticated(false);
            setToken("")
        }
      }, [setIsAuthenticated]);
  
    const handleLogin = (loginToken : string) => {
        setIsAuthenticated(true);
        setToken(loginToken)
      };
    
    const handleLogout = () => {
        setIsAuthenticated(false);
        setToken("");
      };

    const loginParams : loginParamsType = {
        isAuthenticated : isAuthenticated,
        token : token,
        handleLogin : handleLogin,
        handleLogout : handleLogout
    };

    return ( 
        <div className="d-flex flex-column min-vh-100 bg-color1">
            <Header loginParams={loginParams}/>
            <Routes>
                <Route path='/' element={<Home loginParams={loginParams}/>} />
                <Route path='/friends' element={<Friends loginParams={loginParams}/>} />
                <Route path='/group/:group_id' element={<GroupDetails loginParams={loginParams}/>} />
            </Routes>
            <Footer/>
        </div> 
    );
}


export default App;
