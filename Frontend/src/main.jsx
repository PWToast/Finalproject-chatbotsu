import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Registerpage from "../Page/Registerpage.jsx";
import Homepage from "../Page/Homepage.jsx";
import Chatpage from "../Page/Chatpage.jsx";
import DashboardPage from "../Page/DashboardPage.jsx";
import ChatHistoryPage from "../Page/ChatHistoryPage.jsx";
import ManageDataPage from "../Page/ManageDataPage.jsx";
import ViewDocsPage from "../Page/ViewDocsPage.jsx";
import ProtectedRoute from "../component/ProtectedRoute.jsx";
const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "register",
    element: <Registerpage />,
  },
  {
    path: "home",
    element: <Homepage />,
  },
  {
    path: "chat",
    element: (
      <ProtectedRoute allowedRoles={["user", "admin"]}>
        <Chatpage />
      </ProtectedRoute>
    ),
  },
  {
    path: "dashboard",
    element: (
      <ProtectedRoute allowedRoles={["admin"]}>
        <DashboardPage />
      </ProtectedRoute>
    ),
  },
  {
    path: "manage-rag-soures",
    element: (
      <ProtectedRoute allowedRoles={["admin"]}>
        <ManageDataPage />
      </ProtectedRoute>
    ),
  },
  {
    path: "conversation-history",
    element: (
      <ProtectedRoute allowedRoles={["admin"]}>
        <ChatHistoryPage />,
      </ProtectedRoute>
    ),
  },
  {
    path: "view-docs-page",
    element: (
      <ProtectedRoute allowedRoles={["admin"]}>
        <ViewDocsPage />,
      </ProtectedRoute>
    ),
  },
]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
