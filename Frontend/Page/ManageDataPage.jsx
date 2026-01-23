import Adminsidebar from "../component/AdminSidebar"
import { LuHardDriveUpload } from "react-icons/lu";
import { IoSearch } from "react-icons/io5";
import { useState, useRef } from 'react';

function ManageDataPage() {
    const fileInputRef = useRef(null)
    const [files, setFiles] = useState([])

    const handleClickFile = () =>{
        fileInputRef.current.click()
    }
    const handleFileChange = (event) => {
        // .targer.file ปกติแล้วใช้กับปุ่ม input
        const selectedFiles = event.target.files
        if (selectedFiles && selectedFiles.length > 0) {
        console.log("Files selected:", selectedFiles)
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
        const droppedFiles = event.dataTransfer.files
        if (droppedFiles && droppedFiles.length > 0) {
        // จัดการไฟล์ที่ได้ตรงนี้
        console.log("Files dropped:", droppedFiles)
        setFiles([...files, ...Array.from(droppedFiles)])
        }
    }
    return (
        <>
        <div className="flex min-h-screen bg-[#E7E9EB]">
            <Adminsidebar/>
            <main className="m-2 flex-1 overflow-y-auto">
            <div className="flex flex-col w-full h-100 items-center border-2 border-dashed"
            onDragOver={handleDragOver}
            onDrop={handleDrop}
            >         
                <LuHardDriveUpload className="w-10 h-10 mb-5 mt-10"/>
                <p>คลิ๊กปุ่มข้างล่างหรือลากไฟล์มาวางเพื่ออัพโหลด</p>
                <p>รับขนาดไฟล์รวมกันได้สูงสุด 10MB และไม่เกิน 5 ไฟล์ต่อครั้งการอัพโหลด</p>
                <div className="flex flex-row w-32 h-10 bg-amber-300 p-2 rounded-xl mt-5 cursor-pointer hover:bg-amber-600" onClick={handleClickFile}>
                    <IoSearch className="mr-2 mt-1 "/>
                    <button className="pointer-events-none">อัพโหลดไฟล์</button>
                </div>
                <input type="file" className="hidden" ref={fileInputRef} onChange={handleFileChange} multiple/>
                {files.length > 0 && (
                    <div className="mt-4 w-full max-w-md">
                    <p className="font-bold">ไฟล์ที่เลือก:</p>
                    <div className="max-h-30 min-h-30 overflow-auto no-scrollbar border border-gray-300 rounded-lg p-2 bg-white/50">
                        <ul className="list-disc pl-5">
                            {files.map((file, index) => (
                                // truncate จะช่วยตัดคำถ้ายาวเกินบรรทัด
                                <li key={index} className="text-sm text-gray-700 truncate">
                                    {index+1}. {file.name}
                                </li>
                            ))}
                        </ul>   
                    </div>
                    </div>
                )}
            </div>
            </main>
        </div>
        </>   
    )
} 
export default ManageDataPage;