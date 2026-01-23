import Navbar from '../component/navbar'
import { useState, useEffect } from 'react'
import axios from 'axios'
import { CiSettings } from "react-icons/ci";
import { v4 as uuidv4 } from 'uuid';
import { useAuth } from "../service/Auth"
import { jwtDecode } from "jwt-decode";

function Chatpage() {
  const tokenString = localStorage.getItem('token')
  const decoded = jwtDecode(tokenString)
  const emailToken = decoded.email
  useAuth()

  const [inputmessage, setInputMessage] = useState("")
  const [chatroom, setChatRoom] = useState([])
  const [currentSession, setCurrentSession] = useState(null)
  const [currentmessages, setCurrentMessages] = useState([])

  const selectSession = async (session_id) =>{
    console.log("you now selected", session_id)
    setCurrentSession(session_id)
    const res = await axios.get(`http://localhost:8000/fetch/${emailToken}/${session_id}`)
    console.log(res.data.response)
    setCurrentMessages(res.data.response)
  }

  const createNewChatRoom = () => {
    const newRoom ={
      session_id: uuidv4(),
      state: "empty",
      message:[]
    }
    setChatRoom(prev =>[...prev, newRoom])
    setCurrentSession(newRoom.session_id)
    return newRoom.session_id
  }

  const initialHistoryChat = async(currentSession, isNewRoom = false)=>{
    //isNewRoom ค่า default คือ false
    if (!isNewRoom) {
      const selectedRoom = chatroom.find(room=> room.session_id === currentSession)
      // ถ้าหาไม่เจอ หรือสถานะไม่ใช่ empty ให้จบการทำงาน
      if (!selectedRoom || selectedRoom.state !== "empty") return
    }
    setChatRoom(prev =>
      prev.map(room =>
        room.session_id === currentSession
          ? { ...room, state: "active" } // เปลี่ยนแค่ state เป็น active แล้วอัพลง database
          : room
      )
    )
    try{
      const tokenString = localStorage.getItem('token')
      const decoded = jwtDecode(tokenString)
      const email = decoded.email
      const data ={
        email,
        session: currentSession,
        state:"active"
      }
      await axios.post('http://localhost:3000/createsession',data)
      console.log('db update succes!')
    }catch(error){
      alert("error", error)
      console.log(error)
    }
  } 

  async function sendMessage (){
    try{
      let sessionToUse = currentSession
      let isNewSession = false

      if(currentSession === null){
        sessionToUse = createNewChatRoom()
        setCurrentSession(sessionToUse)
        isNewSession = true
      }

      const buffermessage = inputmessage
      setInputMessage('')

      const res = await axios.post('http://localhost:8000/chat_rag_memory', {message: inputmessage, email: emailToken, session_id:sessionToUse})
      const newResponse = {
        user_message:buffermessage, 
        ai_message:res.data.response
      }

      setCurrentMessages(prev=>[...prev, newResponse])

      if (isNewSession) {
         // ถ้าเป็นห้องใหม่ ส่ง true ไปบอกให้ข้ามการเช็ค state
         initialHistoryChat(sessionToUse, true) 
      } else {
         // ถ้าเป็นห้องเก่า ให้ทำงานตามปกติ (ไม่ต้องส่ง true)
         initialHistoryChat(sessionToUse)
      }
    }catch(error){
      alert("error", error)
    }
  }

  const deleteChatRoom = async (session_id) => {
    try{
      const res = await axios.delete(`http://localhost:3000/deletesession?session=${session_id}`)
      setChatRoom(prev => prev.filter(room => room.session_id !== session_id))
      if (currentSession === session_id) {
        setCurrentSession(null)
        setCurrentMessages([])
      }
      console.log('delete success', session_id)
    }catch(error){
      console.error("Delete failed", error)
    }
    setCurrentSession(null)
    console.log('delete success', session_id)
  }

  useEffect(()=>{
    const fetchSessions = async () =>{
      try{
        const tokenString = localStorage.getItem('token')
        const decoded = jwtDecode(tokenString)
        const email = decoded.email
        const res = await axios.get(`http://localhost:3000/getsession?email=${email}`)
        console.log(res.data)
        const sessionsWithMessage = res.data.map(session => ({
          ...session,
          message: []
        }))
        setChatRoom(sessionsWithMessage)
      }catch(error){
        alert("error cannot fetch session", error)
        console.log(error)
      }
    }
    fetchSessions()
  },[])

  return (
    <>
    <div className='flex flex-col h-screen'>
      <Navbar/>
      <div className='pl-10 pt-15 pb-5 w-full'>
        {/*มี 3 ส่วน โดยแบ่ง 15 65 15*/}
        <div className='grid grid-cols-[15%_65%_15%] gap-4 h-full w-full'>

          {/*อันนี้คือส่วนของbar ของ chatroom*/}
          <div className='border border-transparent rounded-xl bg-[#D9D9D9]'>
            <div className='flex flex-col gap-5 p-5'>
              <div className='self-center w-[90%] p-5 border border-transparent bg-[#007A6D] rounded-full text-center text-xl cursor-pointer' onClick={createNewChatRoom}>
                + New Chat
              </div>
              <div className='border-t border-black'></div>
              <div className='ml-9 h-140 w-50 flex flex-col gap-15 overflow-auto no-scrollbar'>
                {chatroom.map((items, index) => (
                  <div className='w-[90%] flex flex-row justify-between font-bold text-xl cursor-pointer hover:bg-[#007A6D]' key={index} onClick={() => selectSession(items.session_id)}>Chat <span className='cursor-pointer text-red-500' onClick={() => deleteChatRoom(items.session_id)}> delete </span></div>
                ))}
              </div>
            </div>
            <div className='flex flex-col gap-5 ml-10 mb-5'>
              <div className=' flex flex-row w-[90%] h-12 p-1 border border-solid rounded-full border-gray-500'>
                <div className='h-10 w-10 bg-[#BEAEAE] rounded-full mr-2'>
                  <CiSettings className='h-8 w-8 mt-1 ml-1'/>
                </div>
                <div className='mt-2'>
                  Settings
                </div>
              </div>
              <div className=' w-[90%] h-12 p-1 border border-solid rounded-full border-gray-500'>
                <div className='mt-2 ml-5'>
                  Profile
                </div>
              </div>
            </div>
          </div>

          {/*อันนี้คือส่วนที่ 2 ของหน้าจอหลักห้องคุย*/}
          <div className=' border-2 border-solid rounded-xl flex flex-col h-215'>

            <div className='flex-1 overflow-auto no-scrollbar flex flex-col gap-2'>
              {currentmessages.map((items, index) => (
                <div key={index} className='flex flex-col gap-2'>
                  <div className='max-w-150 self-end m-5 p-5 bg-[#D9D9D9] border border-transparent rounded-xl'>
                    {items.user_message}
                  </div>
                  <div className='max-w-150 self-start m-5 p-5 bg-[#D9D9D9] border border-transparent rounded-xl'>
                    {items.ai_message}
                  </div>
                </div>
              ))}

            </div>

            <div className='bg-[#D9D9D9] rounded-3xl self-center w-[90%] h-[70px] mb-3'>
              <input
              className='w-[95%] h-full p-5 rounded-3xl outline-none'
              type = "text"
              value={inputmessage}
              onChange={(e)=> setInputMessage(e.target.value)}
              placeholder='พิมพ์คำถามหรือข้อสงสัย...'
              >
              </input>
              <span onClick={()=> sendMessage()}className=' h-full w-full cursor-pointer'>ส่ง</span>
            </div>
          </div>

          {/*ส่วนที่ 3 ส่วนของ Suggestion ไม่มีอะไร กดอะไรไม่ได้*/}
          <div className='border-2 border-solid rounded-xl'>
            <div className='flex flex-col gap-10 p-5'>
              <span className='self-center text-2xl'>Suggestion</span>
              <div className='flex flex-col p-3 '>
                <span className='line-clamp-1'>DSA SU กองกิจการนักศึกษา</span>
                <ul className='list-disc ml-10'>
                  <li><span className='line-clamp-1 text-sm text-gray-500' title="กยศ">กยศ</span></li>
                  <li><span className='line-clamp-1 text-sm text-gray-500' title="หอพักนักศึกษา">หอพักนักศึกษา</span></li>
                </ul>
              </div>
              <div className='flex flex-col p-3'>
                <span className='line-clamp-1'>กองบริหารงานวิชาการ</span>
                <ul className='list-disc ml-10'>
                  <li><span className='line-clamp-1 text-sm text-gray-500' title="ลงทะเบียน">ลงทะเบียน</span></li>
                  <li><span className='line-clamp-1 text-sm text-gray-500' title="เพิ่มถอน">เพิ่มถอน</span></li>
                  <li><span className='line-clamp-1 text-sm text-gray-500' title="การยื่นใบคำร้อง">การยื่นใบคำร้อง</span></li>
                </ul>
              </div>
              <div className='flex flex-col p-3 '>
                <span className='line-clamp-1'>BDT.SU สำนักดิจิทัลเทคโนโลยี</span>
                <ul className='list-disc ml-10'>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </>
  )
}

export default Chatpage