import { useState } from "react"
import { Link, useNavigate} from "react-router-dom"
import { FiEye } from "react-icons/fi";
import { FiEyeOff } from "react-icons/fi";
import { Registerapi } from "../api/Userapi";

function Registerpage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmpassword, setConfirmpassword] = useState("")

  const [typeinputpassword, setTypeinputPassword] = useState("password")
  const [typeinputconfirmpassword, setTypeinputConfirmPassword] = useState("password")
  const [iconpassword, setIconPassword] = useState(false)
  const [iconconfirmpassword, setIconConfirmPassword] = useState(false)

  const isFieldFull = username.trim() && email.trim() && password.trim() && confirmpassword.trim()

    async function handleSubmitFrom(){
        if (!username || !email || !password || !confirmpassword) {
        return alert("กรุณากรอกฟอร์มให้ครบ");
        }
        if(!email.includes("@")){
            return alert("รูปแบบ email ไม่ถูกต้อง")
        }
        if(password !== confirmpassword){
            return alert("รหัสไม่ตรงกัน")
        }
        const User = {
            username,
            email,
            password
        }
        try{
            //const res = await axios.post('http://localhost:3000/register', User)
            const res = await Registerapi(User)
            alert('register success!')
            return navigate("/")
        }catch(error){
            console.log(error.response?.data || error.message)
            alert("something wrong!")
        }
    }

    const handlevisiblePassword = () =>{
        if(typeinputpassword ==='password'){
            setIconPassword(!iconpassword)
            setTypeinputPassword("text")
        }else{
            setIconPassword(!iconpassword)
            setTypeinputPassword("password")
        }
    }
    
    const handlevisibleConfirmPassword = () =>{
        if(typeinputconfirmpassword ==='password'){
            setIconConfirmPassword(!iconconfirmpassword)
            setTypeinputConfirmPassword("text")
        }else{
            setIconConfirmPassword(!iconconfirmpassword)
            setTypeinputConfirmPassword("password")
        }
    }

  return (
    <div className="w-screen h-screen flex flex-col justify-center items-center">
        <div className="flex flex-col items-end w-[600px] h-[550px] bg-[#D9D9D9] border border-transparent rounded-xl shadow-xl/30">
            <span className="self-center text-[25px] mb-5 mt-5">REGISTER FORM</span>
            <div className="flex flex-col h-[300px] w-[600px] justify-between">
                <span className="self-center w-60 mr-10">Username</span>
                <input
                className='bg-[#FFFFFF] p-2 self-center w-60 border border-transparent rounded-md'
                type="text"
                name="username"
                value={username}
                onChange={(e)=>setUsername(e.target.value)}
                >
                </input>

                <span className="self-center w-60 mr-10">Email</span>
                <input
                className='bg-[#FFFFFF] p-2 self-center w-60 border border-transparent rounded-md'
                type="email"
                name="email"
                value={email}
                onChange={(e)=>setEmail(e.target.value)}
                ></input>

                <span className="self-center w-60 mr-10">Password</span>
                <input
                className='bg-[#FFFFFF] p-2 self-center w-60 border border-transparent rounded-md'
                type={typeinputpassword}
                name="password"
                value={password}
                onChange={(e)=>setPassword(e.target.value)}
                ></input>
                <button className="absolute self-center mt-49 ml-53 cursor-pointer" onClick={handlevisiblePassword}>{iconpassword ? <FiEye/> : <FiEyeOff/>}</button>
                <span className="self-center w-60 mr-10">Confirm Password</span>
                <input
                className='bg-[#FFFFFF] p-2 self-center w-60 border border-transparent rounded-md'
                type={typeinputconfirmpassword}
                name="confirmpassword"
                value={confirmpassword}
                onChange={(e)=>setConfirmpassword(e.target.value)}
                ></input>
                <button className="absolute self-center mt-68 ml-53 cursor-pointer" onClick={handlevisibleConfirmPassword}>{iconconfirmpassword ? <FiEye/> : <FiEyeOff/>}</button>
            </div>
            {!isFieldFull &&
            <button className='bg-[#FFFFFF] hover:bg-[#007A6D] transition-colors duration-500 w-80 self-center mt-15 p-3 text-black/50 cursor-pointer' onClick={handleSubmitFrom}>Sign up</button>}
            {isFieldFull && 
            <button className='bg-[#007A6D] transition-colors duration-500 w-80 self-center mt-15 p-3 text-black/50 cursor-pointer' onClick={handleSubmitFrom}>Sign up</button>}
            <div className="text-[12px] self-center mt-2">
                <span>หากมีบัญชีอยู่แล้ว</span><span className='text-[#007A6D] cursor-pointer hover:text-[#006257]'><Link to="/"> เข้าสู่ระบบที่นี่</Link></span>
            </div>
        </div>
    </div>
  )
}

export default Registerpage