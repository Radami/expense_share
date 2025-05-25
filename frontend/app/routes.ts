import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("welcome", "welcome/welcome.tsx"),
    route("auth/login", "auth/Login.tsx"),
    route("auth/logout", "auth/Logout.tsx")

] satisfies RouteConfig;
