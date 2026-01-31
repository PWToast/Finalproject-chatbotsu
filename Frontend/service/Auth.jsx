import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { handleLogout } from "../api/Userapi";
import axios from "axios";

export const useAuth = (requiredRole = null) => {
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        alert("authentication error!");
        navigate("/");
        return;
      }

      try {
        const res = await axios.get("http://localhost:8000/verify", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        console.log(res.data.message);

        const userRole = res.data.role;
        if (requiredRole && userRole !== requiredRole) {
          alert("คุณไม่มีสิทธิ์เข้าถึงหน้านี้!");
          navigate("/"); // หรือหน้าไหนก็ได้ที่ User ปกติเข้าได้
        }
      } catch (error) {
        console.log("authentication errer", error);
        handleLogout();
        navigate("/");
      }
    };

    checkAuth();
  }, [navigate, requiredRole]);
};
