import Navbar from '../component/navbar'
import { useState } from 'react'
import axios from 'axios'
import { CiSettings } from "react-icons/ci";
import { v4 as uuidv4 } from 'uuid';

function Chatpage() {
  const [chatroom, setChatRoom] = useState([])
  const [messagestring, setMessageString] = useState([])
  const [inputmessage, setInputMessage] = useState("")
  const [currentSession, setCurrentSession] = useState("")

  const selectSession = (session) =>{
    console.log("you now selected", session)
    setCurrentSession(currentSession)
  }

  const createNewChatRoom = () => {
    const newRoom ={
      session_id: uuidv4()
    }
    setChatRoom(prev =>[...prev, newRoom])
    console.log(newRoom.session_id)
  }

  const deleteChatRoom = (session_id) => {
    console.log(session_id)
    setChatRoom(prev =>
      prev.filter(room => room.session_id !== session_id)
    )
  }

  async function sendMessage (){
    try{
      const buffermessage = inputmessage
      setInputMessage('')
      const res = await axios.post('http://localhost:7000/chat_rag_memory', {message: inputmessage})
      setMessageString(prev => [...prev,{user_message:buffermessage, ai_message:res.data.response}])
      
    }catch(error){
      alert("error", error)
    }
  }

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
                  <div className='w-[90%] flex flex-row justify-between font-bold text-xl cursor-pointer' key={index} onClick={() => selectSession(items.session_id)}>Chat <span className='cursor-pointer text-red-500' onClick={() => deleteChatRoom(items.session_id)}> delete </span></div>
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
              {messagestring.map((items, index) => (
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
              placeholder='พิมพ์ลงในนี้!'
              >
              </input>
              <span onClick={sendMessage}className=' h-full w-full cursor-pointer'>send</span>
            </div>
          </div>

          {/*ส่วนที่ 3 ส่วนของ Suggestion ไม่มีอะไร กดอะไรไม่ได้*/}
          <div className='border-2 border-solid rounded-xl'>
            <div className='flex flex-col gap-10 p-5'>
              <span className='self-center text-2xl'>Suggestion</span>
              <div className='flex flex-col border-2 border-solid border-gray-500 rounded-2xl p-3 '>
                <span className='line-clamp-1'>DSA|SU กองกิจการนักศึกษา</span>
                <span className='line-clamp-1 text-sm text-gray-500' title="กยศ หอพักนักศึกษา">กยศ หอพักนักศึกษา</span>
              </div>
              <div className='flex flex-col border-2 border-solid border-gray-500 rounded-2xl p-3'>
                <span className='line-clamp-1'>กองบริหารงานวิชาการ</span>
                <span className='line-clamp-1 text-sm text-gray-500' title="ลงทะเบียน เพิ่มถอน การยื่นใบคำร้อง">ลงทะเบียน เพิ่มถอน การยื่นใบคำร้อง</span>
              </div>
              <div className='flex flex-col border-2 border-solid border-gray-500 rounded-2xl p-3'>
                <span className='line-clamp-1'>BDT.SU สำนักดิจิทัลเทคโนโลยี</span>
                <span className='line-clamp-1 text-sm text-gray-500' title="กยศ หอพักนักศึกษา">กยศ หอพักนักศึกษา</span>
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