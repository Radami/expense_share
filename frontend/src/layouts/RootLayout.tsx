import { Outlet } from "react-router-dom";
import Footer from "./Footer";
import Header from "./Header";

function RootLayout() {
  return (
    <div className="d-flex flex-column min-vh-100 bg-color">
        <Header />
        <div className="container col-lg-6">
            <main>
                <Outlet />
            </main>
        </div>
        <Footer />
    </div>
  );
}

export default RootLayout;