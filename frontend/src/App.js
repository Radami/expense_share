import { useEffect } from 'react';
import './App.css';
import Footer from "./components/footer";
import Header from "./components/header";

function App() {
    useEffect( () => {
    })
  
    return (
      <div className="d-flex flex-column min-vh-100 bg-dark">
        <Header />
        <Footer />
      </div>
    );
}

export default App;
