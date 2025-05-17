import { createBrowserRouter, type RouteObject } from "react-router-dom";

import Login from "./auth/Login";
import Logout from "./auth/Logout";
import Profile from "./auth/Profile";
import RootLayout from "./layouts/RootLayout"; // Your main layout component (e.g., has <Outlet />)
import AddExpensePage from "./pages/AddExpensePage";
import AddGroupPage from "./pages/AddGroupPage";
import GroupDetailsPage from "./pages/GroupDetailsPage";
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
            {
                path: "add_group",
                element: <AddGroupPage />,
            },
            {
                path: "group/:group_id",
                element: <GroupDetailsPage />
            },
            {
                path: "add_expense/:group_id?",
                element: <AddExpensePage />
            }
        ],

    },
    {
        path: "/auth",
        element: <RootLayout />,
        errorElement: <NotFoundPage />,
        children: [
            { path: "login", element: <Login />},
            { path: "logout", element: <Logout />},
            { path: "profile", element: <Profile />}
        ]
    }
]

const router = createBrowserRouter(routes);

export default router;