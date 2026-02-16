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
import EditPromptPage from "../Page/EditPromptPage.jsx";
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
    element: <Chatpage />,
  },
  {
    path: "dashboard",
    element: <DashboardPage />,
  },
  {
    path: "manage-rag-soures",
    element: <ManageDataPage />,
  },
  {
    path: "conversation-history",
    element: <ChatHistoryPage />,
  },
  {
    path: "view-docs-page",
    element: <ViewDocsPage />,
  },
  {
    path: "edit-prompt",
    element: <EditPromptPage />,
  },
]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
