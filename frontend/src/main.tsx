import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import './index.css'; // Your global CSS
import router from './router'; // Import your new router!

// 1. Import Bootstrap's CSS
import 'bootstrap/dist/css/bootstrap.min.css'; // The minified CSS is usually preferred

// 2. (Optional) Import Bootstrap Icons if you're using them directly
// You already have "bootstrap-icons" in package.json
import 'bootstrap-icons/font/bootstrap-icons.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);