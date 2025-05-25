import { Outlet } from "react-router-dom";
import Footer from "./Footer";
import Header from "./Header";

function RootLayout() {
  return (
    <div className="d-flex flex-column min-vh-100 bg-color1">
      <Header />
      <main>
        <Outlet /> {/* This is where nested routes will render */}
      </main>
      <Footer />
    </div>
  );
}

export default RootLayout;