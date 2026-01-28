import Adminsidebar from "../component/AdminSidebar";
import { LuHardDriveUpload } from "react-icons/lu";
import { IoSearch } from "react-icons/io5";
import { useState, useRef, Activity } from "react";
import axios from 'axios'
function ManageDataPage() {
  const [activeTab, setActiveTab] = useState('uploadfile')
  const fileInputRef = useRef(null)
  const contentFileRef = useRef(null)
  const [contentfilename, setContentFileName] = useState("ไม่ได้เลือกไฟล์ สามารถอัพโหลดไฟล์ .txt ได้")
  const [files, setFiles] = useState([])

  const [content, setContent] = useState("")
  const [topic, setTopic] = useState("")
  const [category, setCategory] = useState("") 
  const [agency, setAgency] = useState("กองบริหารวิชาการ") 
  const [source, setSource] = useState("")

  const handleClickFile = () => {
    fileInputRef.current.click()
  }
  const handleFileChange = (event) => {
    // .targer.file ปกติแล้วใช้กับปุ่ม input
    const selectedFiles = event.target.files;
    if (selectedFiles && selectedFiles.length > 0) {
      console.log("Files selected:", selectedFiles);
      // Array.from แปลงfilelist ให้กลายเป็น array จริงๆก่อน
      setFiles([...files, ...Array.from(selectedFiles)])
    }
  }
  const handleDragOver = (event) => {
    //อนุญาติให้พื้นที่ตรงนี้ ... ลากไฟล์มาวางได้
    event.preventDefault()
  }
  const handleDrop = (event) => {
    event.preventDefault()
    // .dataTransfer.file ใช้กับการลากวาง
    const droppedFiles = event.dataTransfer.files;
    if (droppedFiles && droppedFiles.length > 0) {
      // จัดการไฟล์ที่ได้ตรงนี้
      console.log("Files dropped:", droppedFiles)
      setFiles([...files, ...Array.from(droppedFiles)])
    }
  }
  const handlesubmitFileUpload = async () =>{
    const allowed_types = ["application/pdf", "text/plain"]
    const max_size_mb = 10
    const totalSize = files.reduce((sum, file) => sum + file.size, 0)
    const limitSize = 1024 * 1024 * max_size_mb
    if(files.length > 5){
      setFiles([])
      return alert("ส่งไฟล์ได้ไม่เกิน 5 ไฟล์ต่อครั้ง")
    }
    if(totalSize > limitSize){
      setFiles([])
      return alert("ขนาดไฟล์มีขนาดเกิน 10 mb") 
    }
    for(const file of files){
      if(!allowed_types.includes(file.type)){
        setFiles([])
        return alert("ฟอร์มนี้รับเฉพาะไฟล์ประเภท txt และ pdf เท่านั้น")
      }
    }
    try{
      console.log("รูปแบบไฟล์ถูกต้องกำลังส่ง")
      //for each ในตัวแปร files เพื่อใส่เข้า object FormData แล้วส่งผ่าน api 
      //เนื่องจาก Array.form ไม่ได้ทำให้ข้อมูลข้างในเปลี่ยนไปเลยสามารถทำท่านี้ตรงๆได้
      for(const file of files){
        const formData = new FormData()
        // 'fileupload คือ key ที่ map ให้ตรง key ใน backend เฉยๆ
        formData.append('fileupload', file)
        const res = await axios.post('http://localhost:8000/upload', formData,{
          //บอก labelของข้อมูลผ่าน header เฉยๆ
          headder:{
            'Content-Type' : 'multipart/form-data'
          }
        })
      }
    }catch(error){
      console.log(error)
      alert("error", error)
    }
  }
  const clearFileUploadForm = () =>{
    setFiles([])
  }
  function DateTime() {
    //.padStart(2,"0") คือเติมอักษร string ด้านหน้าให้ string ยาวตามที่กำหนด parameter ตัวแรกคือ จำนวนที่ต้องการเติม และ อักษระstringที่ต้องการ
    const now = new Date();
    const formatted =
      `${String(now.getDate()).padStart(2, "0")}/` +
      `${String(now.getMonth() + 1).padStart(2, "0")}/` +
      `${now.getFullYear()} ` +
      `${String(now.getHours()).padStart(2, "0")}:` +
      `${String(now.getMinutes()).padStart(2, "0")}`

      return formatted
  }

  const handlesubmitTextForm = async () =>{
    const form_to_send = {
      "content": content,
      "metadata" :{
        "topic":topic,
        "category":category,
        "agency":agency,
        "source":source,
        "added_at": DateTime()
      }
    }
    try{
      const res = await axios.post("http://localhost:8000/textupload", form_to_send)
    }catch(error){
      console.log("something wrong", error)
    }
    console.log("send form succcess!")
  }

  const handlefileuploadtocontentform = (e) =>{
    const file = e.target.files[0]
    if(!file)
      return

    const reader = new FileReader()

    reader.onload = (event) => {
      setContent(event.target.result) //เอาเนื้อหาไฟล์ text มาแสดงในตัวแปร content
      setContentFileName(file.name)
    }
    reader.readAsText(file, "UTF-8")
    e.target.value = null
  }

  return (
    <>
      <div className="flex min-h-screen bg-[#E7E9EB]">
        <Adminsidebar />
        <main className="m-2 flex-1 overflow-y-auto w-full">

          <div className="flex flex-col w-full">
            <div className="flex justify-center">
              <div className="overflow-hidden w-70 bg-[#007A6D] m-5 rounded-2xl grid grid-cols-2 divide-x-2 divide divide-black-500">
                <button onClick={()=>setActiveTab('uploadfile')} className=" cursor-pointer self-center p-5 
                active:bg-teal-600 focus:bg-teal-600 hover:bg-teal-600 text-white
                ">อัพโหลดไฟล์</button>
                <button onClick={()=>setActiveTab('formfield') } className=" cursor-pointer self-center p-5
                active:bg-teal-600 focus:bg-teal-600 hover:bg-teal-600 text-white
                ">กรอกฟอร์ม</button>
              </div>
            </div>

          </div>
          <Activity mode ={activeTab ==='uploadfile' ? 'visible' : 'hidden'}>
            <div
            className="flex flex-col w-full h-110 items-center border-2 border-dashed"
            onDragOver={handleDragOver}
            onDrop={handleDrop}
            >
            <LuHardDriveUpload className="w-10 h-10 mb-5 mt-10" />
            <p>คลิ๊กปุ่มข้างล่างหรือลากไฟล์มาวางเพื่ออัพโหลด</p>
            <p>รับขนาดไฟล์รวมกันได้สูงสุด 10MB และไม่เกิน 5 ไฟล์ต่อครั้งการอัพโหลด</p>
            <p>สามารถส่งได้แค่ไฟล์ .txt และ pdf เท่านั้น</p>
            <div className="flex flex-row w-32 h-10 bg-amber-300 p-2 rounded-xl mt-5 cursor-pointer hover:bg-amber-600" onClick={handleClickFile}>
              <IoSearch className="mr-2 mt-1 " />
              <button className="pointer-events-none">อัพโหลดไฟล์</button>
            </div>
            <input
              type="file"
              className="hidden"
              ref={fileInputRef}
              onChange={handleFileChange}
              multiple
            />
            {files.length > 0 && (
              <div className="mt-4 w-full max-w-md">
                <p className="font-bold">ไฟล์ที่เลือก:</p>
                <div className="max-h-30 min-h-30 overflow-auto no-scrollbar border border-gray-300 rounded-lg p-2 bg-white/50">
                  <ul className="list-disc pl-5">
                    {files.map((file, index) => (
                      // truncate จะช่วยตัดคำถ้ายาวเกินบรรทัด
                      <li
                        key={index}
                        className="text-sm text-gray-700 truncate"
                      >
                        {index + 1}. {file.name}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
          <button className="bg-[#EE4B2B] hover:bg-red-600 cursor-pointer text-white px-8 py-3 m-5 rounded-2xl" onClick={clearFileUploadForm}>ยกเลิกและล้างฟอร์ม</button>
          <button className="bg-[#007A6D] hover:bg-teal-600 cursor-pointer text-white px-8 py-3 m-5 rounded-2xl" onClick={handlesubmitFileUpload}>ยืนยัน</button>
          </Activity>

          <Activity mode ={activeTab ==='formfield' ? 'visible' : 'hidden'}>
            <div className="flex flex-col items-center justify-center w-full p-4">
  
              <div className="flex flex-col w-full max-w-2xl gap-6"> 
                
                <div className="flex flex-col w-full"> 
                  <p className="font-semibold mb-1">เนื้อหา</p>
                  <textarea className="bg-white w-full h-25 shadow-xl p-2 rounded-md" name="content" value={content} onChange={(e)=>setContent(e.target.value)}/>
                  <div className="mt-2 max-w-90 cursor-pointer px-8 py-3 rounded-2xl hover:bg-[#007A6D] hover:text-white" onClick={()=>contentFileRef.current.click()}>
                    <span>{contentfilename}</span>
                    <input type="file" className="hidden" accept=".txt" onChange={handlefileuploadtocontentform} ref={contentFileRef}/>
                  </div>
                </div>

                <div className="flex flex-col w-full"> 
                  <p className="font-semibold mb-1">หัวข้อ</p>
                  <textarea className="bg-white w-full h-25 shadow-xl p-2 rounded-md" name="topic" value={topic} onChange={(e)=>setTopic(e.target.value)}/>
                </div>

                <div className="flex flex-col w-full"> 
                  <p className="font-semibold mb-1">ประเภทของเนื้อหา</p>
                  <textarea className="bg-white w-full h-25 shadow-xl p-2 rounded-md" name="topic" value={category} onChange={(e)=>setCategory(e.target.value)}/>
                </div>

                <div className="flex flex-col w-full">
                  <p className="font-semibold mb-1">หน่วยงานที่เกี่ยวข้อง</p>
                  <select name="agency" className="w-full md:w-64 shadow-xl p-2 rounded-md" value={agency} onChange={(e)=>setAgency(e.target.value)}>
                    <option value="กองบริหารวิชาการ">กองบริหารวิชาการ</option>
                    <option value="กองกิจการนักศึกษา">กองกิจการนักศึกษา</option>
                    <option value="สำนักดิจิทัล">สำนักดิจิทัล</option>
                  </select>
                </div>

                <div className="flex flex-col w-full"> 
                  <p className="font-semibold mb-1">แหล่งที่มา</p>
                  <textarea className="bg-white w-full h-25 shadow-xl p-2 rounded-md" name="source" value={source} onChange={(e)=>setSource(e.target.value)}/>
                </div>

                <div className="flex justify-center mt-4">
                  <button className="bg-[#007A6D] hover:bg-teal-600 cursor-pointer text-white px-8 py-3 rounded-2xl transition-all" onClick={handlesubmitTextForm}>
                    ยืนยัน
                  </button>
                </div>

              </div>
            </div>
          </Activity>

        </main>
      </div>
    </>
  );
}
export default ManageDataPage;
