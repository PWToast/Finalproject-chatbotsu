import axios from "axios";

export const Loginapi = (user) => {
    return axios.post('http://localhost:8000/login', user)
}

export const Registerapi = (user) => {
    return axios.post('http://localhost:8000/register', user)
}

export const handleLogout = () =>{
    localStorage.removeItem('token')
}