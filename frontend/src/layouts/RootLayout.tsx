import { Outlet } from "react-router-dom";
import Footer from "./Footer";
import Header from "./Header";

function RootLayout() {
  return (
    <div className="d-flex flex-column min-vh-100 bg-color1">
        <div className="container col-lg-4 mt-3 ">    
            <Header />
            <main>
                <Outlet /> {/* This is where nested routes will render */}
            </main>
        </div>
        <Footer />
    </div>
  );
}

export default RootLayout;