import { Navigate } from "react-router-dom";

function ProtectedRoute({ children, allowedRoles }) {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (!token) {
    // ถ้าไม่มี Token ให้ไล่กลับไปหน้า Login (หรือ Home)
    return <Navigate to="/" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
    // ถ้า Role ไม่ตรงกับที่มีสิทธิ์ ให้ดีดออกไปหน้าอื่น เช่น /chat
    return <Navigate to="/chat" replace />;
  }

  return children;
}

export default ProtectedRoute;
