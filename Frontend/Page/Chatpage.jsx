import Navbar from "/component/navbar";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { CiLogout } from "react-icons/ci";
import { v4 as uuidv4 } from "uuid";
import { useAuth } from "../service/Auth";
import { jwtDecode } from "jwt-decode";
import { Navigate, useNavigate } from "react-router-dom";
import LogOutModal from "../component/LogOutModal";
import { RiDeleteBin6Fill } from "react-icons/ri";

function Chatpage() {
  const [IsModalOpen, setIsModalOpen] = useState(false)
  const navigate = useNavigate()
  const tokenString = localStorage.getItem("token")
  const decoded = jwtDecode(tokenString)
  const emailToken = decoded.email
  const usernameToshow = decoded.username
  useAuth()

  const [inputmessage, setInputMessage] = useState("")
  const [chatroom, setChatRoom] = useState([])
  const [currentSession, setCurrentSession] = useState(null)
  const [currentmessages, setCurrentMessages] = useState([])
  const messagesEndRef = useRef(null)

  //เอาไว้ให้ uxui ดู smooth เมื่อคุยแล้วให้ scroll เลื่อนลงมายังข้อความล่าสุด
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }
  useEffect(() => {
    scrollToBottom()
  }, [currentmessages])

  const handleLogoutConfirm = () => {
    localStorage.removeItem("token")
    console.log("ออกจากระบบแล้ว!")
    setIsModalOpen(false)
    navigate("/")
  }

  const selectSession = async (session_id) => {
    console.log("you now selected", session_id)
    setChatRoom((prev) => prev.map((room) => ({...room,
        // ถ้า session_id ตรงกันให้เป็น true ถ้าไม่ตรงให้เป็น false
        isSelect: room.session_id === session_id 
      }))
    )
    setCurrentSession(session_id)
    const res = await axios.get(
      `http://localhost:8000/fetch/${emailToken}/${session_id}`,
    )
    console.log(res.data.response)
    setCurrentMessages(res.data.response)
  }

  const createNewChatRoom = () => {
    const newRoom = {
      session_id: uuidv4(),
      state: "empty",
      message: [],
      isSelect: false
    }
    setChatRoom((prev) => [...prev, newRoom])
    setCurrentSession(newRoom.session_id)
    return newRoom.session_id
  }

  const initialHistoryChat = async (currentSession, isNewRoom = false) => {
    //isNewRoom ค่า default คือ false
    if (!isNewRoom) {
      const selectedRoom = chatroom.find(
        (room) => room.session_id === currentSession,
      )
      // ถ้าหาไม่เจอ หรือสถานะไม่ใช่ empty ให้จบการทำงาน
      if (!selectedRoom || selectedRoom.state !== "empty") return
    }
    setChatRoom((prev) =>
      prev.map((room) =>
        room.session_id === currentSession
          ? { ...room, state: "active" } // เปลี่ยนแค่ state เป็น active แล้วอัพลง database
          : room,
      ),
    )
    try {
      const tokenString = localStorage.getItem("token")
      const decoded = jwtDecode(tokenString)
      const email = decoded.email
      const data = {
        email,
        session_id: currentSession,
        state: "active",
      }
      await axios.post("http://localhost:8000/createsession", data)
      console.log("db update succes!")
    } catch (error) {
      alert("error", error)
      console.log(error)
    }
  }

  async function sendMessage() {
    try {
      let sessionToUse = currentSession
      let isNewSession = false

      if (currentSession === null) {
        sessionToUse = createNewChatRoom()
        setCurrentSession(sessionToUse)
        isNewSession = true
      }

      const buffermessage = inputmessage
      setInputMessage("")

      const res = await axios.post("http://localhost:8000/chat_rag_memory", {
        message: inputmessage,
        email: emailToken,
        session_id: sessionToUse,
      })
      const newResponse = {
        user_message: buffermessage,
        ai_message: res.data.response,
      }

      setCurrentMessages((prev) => [...prev, newResponse])

      if (isNewSession) {
        // ถ้าเป็นห้องใหม่ ส่ง true ไปบอกให้ข้ามการเช็ค state
        initialHistoryChat(sessionToUse, true)
      } else {
        // ถ้าเป็นห้องเก่า ให้ทำงานตามปกติ (ไม่ต้องส่ง true)
        initialHistoryChat(sessionToUse)
      }
    } catch (error) {
      alert("error", error)
    }
  }

  const deleteChatRoom = async (session_id) => {
    const roomToDelete = chatroom.find((room) => room.session_id === session_id)

    if (!roomToDelete) return
    //เอาไว้ลบ chatroom ที่ไม่ได้เก็บลง database จะได้แสดงผลทันทีในหน้า ui
    const removeRoomFromUI = () => {
      setChatRoom((prev) => prev.filter((room) => room.session_id !== session_id))
      if (currentSession === session_id) {
        setCurrentSession(null)
        setCurrentMessages([])
      }
    }
    if (roomToDelete.state === "empty") {
      removeRoomFromUI()
      return
    }
    try {
      await axios.delete(`http://localhost:8000/deletesession/${session_id}`)
      // ลบสำเร็จ ค่อยมาลบใน UI
      removeRoomFromUI()
      console.log("Delete success from DB", session_id)
    } catch (error) {
      console.error("Delete failed", error)
      alert("ลบข้อมูลผิดพลาด")
    }
  }

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const tokenString = localStorage.getItem("token")
        const decoded = jwtDecode(tokenString)
        const email = decoded.email
        const res = await axios.get(`http://localhost:8000/getsession/${email}`)
        console.log(res.data)
        const sessionsWithMessage = res.data.map((session) => ({
          ...session,
          message: [],
        }))
        setChatRoom(sessionsWithMessage)
      } catch (error) {
        alert("error cannot fetch session", error)
        console.log(error)
      }
    }
    fetchSessions()
  }, [])

  return (
    <>
      <div className="flex flex-col h-screen">
        <Navbar />
        <div className="pt-15 pb-5 w-full">
          {/*มี 3 ส่วน โดยแบ่ง 15 65 15*/}
          <div className="grid grid-cols-[15%_65%_17%] gap-4 h-full w-full">
            {/*อันนี้คือส่วนของbar ของ chatroom*/}
            <div className="border border-transparent rounded-r-xl bg-[#D9D9D9] h-215 w-20%">
              <div className="flex flex-col gap-5 p-5">
                <div
                  className="self-center w-[90%] p-5 border border-transparent bg-[#007A6D] rounded-full text-center text-xl cursor-pointer"
                  onClick={createNewChatRoom}
                >
                  + New Chat
                </div>
                <div className="border-t border-black"></div>
                <div className=" h-140 w-full flex flex-col gap-5 overflow-auto no-scrollbar">
                  {chatroom.map((items, index) => (
                    <div className="flex flex-col">
                      <div
                        className={`h-10 flex flex-row items-center justify-between font-bold text-xl cursor-pointer rounded-4xl p-5 transition-all ${
                          items.isSelect 
                            ? 'bg-[#00897B] text-white' // สีเมื่อถูกเลือก
                            : ' hover:bg-[#FFFBDE]' // สีปกติ
                        }`}
                        key={index}
                        onClick={() => selectSession(items.session_id)}
                      >
                        <span>Chat</span>
                        <div class={`cursor-pointer rounded-full p-3 transition-colors 
                          ${items.isSelect 
                          ? "hover:bg-white/20 text-teal-100 hover:text-white" 
                          : "hover:bg-red-100 text-red-500"
                          }`} onClick={(e) => {e.stopPropagation();deleteChatRoom(items.session_id)}}>
                            <RiDeleteBin6Fill className="w-6 h-6" />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <div className="flex flex-col gap-5 ml-10 mb-5">
                <div className=" flex flex-row w-[90%] h-12 p-1 border border-solid rounded-full border-gray-500 cursor-pointer">
                  <div className="h-10 w-10 bg-[#BEAEAE] rounded-full mr-2">
                    <CiLogout className="h-8 w-8 mt-1 ml-1" />
                  </div>
                  <button onClick={() => {setIsModalOpen(true)}} className="cursor-pointer">
                    ออกจากระบบ
                  </button>
                </div>
                <div className=" w-[90%] h-12 p-1 border border-solid rounded-full border-gray-500">
                  <div className="mt-2 ml-5">{usernameToshow}</div>
                </div>
              </div>
            </div>

            {/*อันนี้คือส่วนที่ 2 ของหน้าจอหลักห้องคุย*/}
            <div className=" border-2 border-solid rounded-xl flex flex-col h-215 ml-10">
              <div className="flex-1 overflow-auto no-scrollbar flex flex-col gap-2">
                {currentmessages.map((items, index) => (
                  <div key={index} className="flex flex-col gap-2">
                    <div className="max-w-150 self-end m-5 p-5 bg-[#D9D9D9] border border-transparent rounded-xl">
                      {items.user_message}
                    </div>
                    <div className="max-w-150 self-start m-5 p-5 bg-[#D9D9D9] border border-transparent rounded-xl">
                      {items.ai_message}
                    </div>
                  </div>
                ))}
                <div ref={messagesEndRef}/>
              </div>

              <div className="bg-[#D9D9D9] rounded-3xl self-center w-[90%] h-[70px] mb-3">
                <input
                  className="w-[95%] h-full p-5 rounded-3xl outline-none"
                  type="text"
                  value={inputmessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyDown={(e)=> {
                    if (e.key === "Enter"){
                      sendMessage()
                    }
                  }}
                  placeholder="พิมพ์คำถามหรือข้อสงสัย..."
                ></input>
                <span
                  onClick={() => sendMessage()}
                  className=" h-full w-full cursor-pointer"
                >
                  ส่ง
                </span>
              </div>
            </div>

            {/*ส่วนที่ 3 ส่วนของ Suggestion ไม่มีอะไร กดอะไรไม่ได้*/}
            <div className="">
                <div className="border-2 border-solid rounded-xl h-215 overflow-auto no-scrollbar">
                  <div className="flex flex-col gap-3 p-5">
                    <span className="self-center text-2xl">Suggestion</span>
                    <div className="flex flex-col p-3 ">
                      <span className="line-clamp-1">กองบริหารงานวิชาการ</span>
                      <ul className="list-disc ml-10">
                        <li><span className="line-clamp-1 text-sm text-gray-500" title="ขั้นตอนการลงทะเบียนเรียน">ขั้นตอนการลงทะเบียนเรียน </span></li>
                        <li><span className="line-clamp-1 text-sm text-gray-500" title="การลงทะเบียนเรียน (ล่าช้า)">การลงทะเบียนเรียน (ล่าช้า)</span></li>
                        <li><span className="line-clamp-1 text-sm text-gray-500" title="การเพิ่มถอน เปลี่ยนกลุ่มเรียน">การเพิ่มถอน เปลี่ยนกลุ่มเรียน</span></li>
                        <li><span className="line-clamp-1 text-sm text-gray-500" title="การดูผลการลงทะเบียนเรียน">การดูผลการลงทะเบียนเรียน</span></li>
                        <li><span className="line-clamp-1 text-sm text-gray-500" title="ตรวจสอบภาระค่าใช้จ่าย">ตรวจสอบภาระค่าใช้จ่าย</span></li>
                        <li><span className="line-clamp-1 text-sm text-gray-500" title="การขอสำรองที่นั่งออนไลน์">การขอสำรองที่นั่งออนไลน์</span></li>
                        <li><span className="line-clamp-1 text-sm text-gray-500" title="คำร้องขอติด W ออนไลน์">คำร้องขอติด W ออนไลน์</span></li>
                        <li><span className="line-clamp-1 text-sm text-gray-500" title="ตรวจสอบคำร้อง">ตรวจสอบคำร้อง</span></li>
                        <li><span className="line-clamp-1 text-sm text-gray-500" title="Email แจ้งเตือนคำร้อง">Email แจ้งเตือนคำร้อง</span></li>
                        <li><span className="text-sm text-gray-500" title="ใบคำร้องสำหรับนักศึกษาปริญญาตรี">ใบคำร้องสำหรับนักศึกษาปริญญาตรี</span></li>
                      </ul>
                    </div>
                    <div className="flex flex-col p-3">
                      <span className="line-clamp-1">DSA SU กองกิจการนักศึกษา</span>
                      <ul className="list-disc ml-10">
                        <li><span className="text-sm text-gray-500" title="คุณสมบัติของผู้กู้ยืมกยศ.(กู้ยืมเพื่อการศึกษา)">คุณสมบัติของผู้กู้ยืมกยศ.(กู้ยืมเพื่อการศึกษา) </span></li>
                        <li><span className="line-clamp-1 text-sm text-gray-500" title="ประเภทของผู้กู้ยืมเงิน ">ประเภทของผู้กู้ยืมเงิน</span></li>
                        <li><span className="text-sm text-gray-500" title="คุณสมบัติทั่วไปของนักศึกษาผู้กู้ยืมเงินกองทุน">คุณสมบัติทั่วไปของนักศึกษาผู้กู้ยืมเงินกองทุน</span></li>
                        <li><span className="text-sm text-gray-500" title="ลักษณะต้องห้ามของนักศึกษาผู้กู้ยืมเงินกองทุน ">ลักษณะต้องห้ามของนักศึกษาผู้กู้ยืมเงินกองทุน</span></li>
                        <li><span className="text-sm text-gray-500" title="คุณสมบัติเฉพาะของนักศึกษาผู้กู้ยืมเงินกองทุน ลักษณะที่ 1,2 และ 3">คุณสมบัติเฉพาะของนักศึกษาผู้กู้ยืมเงินกองทุน ลักษณะที่ 1,2 และ 3</span></li>
                        <li><span className="line-clamp-1 text-sm text-gray-500" title="หอพักนักศึกษา">หอพักนักศึกษา</span></li>
                      </ul>
                    </div>
                    <div className="flex flex-col p-3 ">
                      <span className="line-clamp-1">BDT.SU สำนักดิจิทัลเทคโนโลยี</span>
                      <ul className="list-disc ml-10">
                        <li><span className="line-clamp-1 text-sm text-gray-500" title="วิธีกู้คืน SU-IT Account">วิธีกู้คืน SU-IT Account</span></li>
                        <li><span className="text-sm text-gray-500" title="วิธีลงทะเบียน SU-IT Account"> วิธีลงทะเบียน SU-IT Account</span></li>
                      </ul>
                    </div>
                  </div>
                </div>
            </div>
          </div>
        </div>
        <LogOutModal
          isModalOpen={IsModalOpen}
          onClose={() => setIsModalOpen(false)}
          onConfirm={handleLogoutConfirm}
        />
      </div>
    </>
  );
}

export default Chatpage;
