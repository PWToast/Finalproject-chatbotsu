import { useState } from "react"
import { FiEye } from "react-icons/fi";
import { FiEyeOff } from "react-icons/fi";
import { Link, useNavigate} from "react-router-dom"
import { Loginapi } from "../api/Userapi";


function Loginfrom() {
    const navigate = useNavigate()
    const [email, setEmail] = useState("")
    const [typeinput, setTypeinput] = useState("password")
    const [password, setPassword] = useState("")
    const [icon, setIcon] = useState(false)
    const isFieldFull = email.trim() && password.trim()
    
    const handlevisiblepassword = () =>{
        if(typeinput ==='password'){
            setIcon(!icon)
            setTypeinput("text")
        }else{
            setIcon(!icon)
            setTypeinput("password")
        }
    }
    async function handleSubmitFrom(){
        const User = {
          email,
          password
        }
        try{
            //const res = await axios.post('http://localhost:3000/login', user)
            const res = await Loginapi(User)
            alert('login success!')
            localStorage.setItem('token', res.data.token)
            return navigate("/home")
        }catch(error){
            console.log(error.response?.data || error.message)
            alert("something wrong!")
        }
    }

  return (
    <>
        <span className='text-[50px] self-center absolute pt-20'>SU Chatbot FAQ</span>
        <div className='h-190 flex flex-row gap-10 justify-center items-center'>
            <div className='h-90 w-100 bg-[#D9D9D9] border border-transparent rounded-xl shadow-xl/30'>
              <div className='h-75 flex flex-col justify-between'>
                <div className='flex flex-col'>
                  <span className='mt-3 ml-5 mb-2'>Email</span>
                  <input 
                  className='bg-[#FFFFFF] p-2 w-80 self-center border border-transparent rounded-md'
                  type="email"
                  name="email"
                  value={email}
                  onChange={(e)=> setEmail(e.target.value)}
                  />
                  <span className='mt-5 ml-5 mb-2'>Password</span>
                  <input
                  className='bg-[#FFFFFF] p-2 w-80 self-center border border-transparent rounded-md' 
                  type ={typeinput}
                  name="password"
                  value={password}
                  onChange={(e)=> setPassword(e.target.value)}
                  />
                  <button className=" absolute self-end-safe mr-11 mt-38 cursor-pointer" onClick={handlevisiblepassword}>{icon ? <FiEye/> : <FiEyeOff/>}</button>
                </div>
                <div className='flex flex-col mb-8 w-100'>
                  <span className='text-[#007A6D] self-end-safe mr-10 mb-1 text-[12px] cursor-pointer hover:text-[#006257]'>ลืมรหัสผ่าน?</span>
                  {!isFieldFull &&
                  <button className='bg-[#FFFFFF] hover:bg-[#007A6D] transition-colors duration-500 w-80 self-center mt-15 p-3 text-black/50 cursor-pointer' onClick={handleSubmitFrom}>Sign in</button>}
                  {isFieldFull && 
                  <button className='bg-[#007A6D] transition-colors duration-500 w-80 self-center mt-15 p-3 text-black/50 cursor-pointer' onClick={handleSubmitFrom}>Sign in</button>}
                  <div className='flex flex-row gap-2 self-center text-[12px] mt-1'>
                    <span>ยังไม่มีบัญชี?</span><span className='text-[#007A6D] cursor-pointer hover:text-[#006257]'><Link to="/register">ลงทะเบียน</Link></span>
                  </div>
                </div>
              </div>
            </div>
            <img className='h-100 w-100' src="/image/logo.png"/>
        </div>
    </>
  )
}

export default Loginfrom