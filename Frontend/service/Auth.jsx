import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { handleLogout } from "../api/Userapi"
import axios from "axios";

export const useAuth = () => {

  const navigate = useNavigate()  

  useEffect(()=>{ 
    const checkAuth = async() =>{
      const token = localStorage.getItem('token')

      if(!token){
        alert('authentication error!')
        navigate('/')
      }

      try{
        const res = await axios.get('http://localhost:8000/verify',{
          headers:{
            'Authorization' : `Bearer ${token}`
          }
        })

        console.log(res.data.message)

      }catch(error){
        console.log("authentication errer", error)
        handleLogout()
        navigate('/')
      }
    }

    checkAuth()

  }, [navigate])
}