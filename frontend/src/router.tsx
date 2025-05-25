import { createBrowserRouter, type RouteObject } from "react-router-dom";

import RootLayout from "./layouts/RootLayout"; // Your main layout component (e.g., has <Outlet />)
import HomePage from "./pages/HomePage";
import NotFoundPage from "./pages/NotFoundPage";

const routes: RouteObject[] = [
    {
        path: "/",
        element: <RootLayout />, // Your main layout wraps all children
        errorElement: <NotFoundPage />, // Catch any errors in this route segment or its children
        children: [
            {
            index: true, // This makes HomePage the default child of '/'
            element: <HomePage />,
            },
        ]
    }
]

const router = createBrowserRouter(routes);

export default router;