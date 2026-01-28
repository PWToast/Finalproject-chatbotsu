import AdminSidebar from "../component/AdminSidebar"
import axios from 'axios'
import { useState, useEffect } from "react"
import { RiDeleteBin6Fill } from "react-icons/ri";
import ViewDataModal from "../component/ViewDataModal"

function ViewDocsPage() {
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [showVieweModal, setShowViewModal] = useState(false)
  const [deleteId, setDeleteId] = useState(null)
  const [contentToView, setContentToView] = useState({
    "content":"",
    "metadata":{
      "topic":"",
      "category":"",
      "agency":"",
      "source":"",
      "added_at":""
    }
  }) 
  const [contentToDelete, setContentToDelete] = useState({
    "content":"",
    "metadata":{
      "topic":"",
      "category":"",
      "agency":"",
      "source":"",
      "added_at":""
    }
  })
  const fetchData = async()=>{
    try{
      const res = await axios.get('http://localhost:8000/getalldocs')
      setData(res.data.docs)
    }catch(error){
      console.log(error)
    }
  }
  const handleViewModalopen = (item) =>{
    setContentToView({
      "content":item.content,
      "metadata":{
        "topic":item.metadata.topic,
        "category":item.metadata.category,
        "agency":item.metadata.agency,
        "source":item.metadata.source,
        "added_at":item.metadata.added_at
      }
    })
    setShowViewModal(true)
  }
  const handleDeleteModalopen = (item) =>{
    setContentToDelete({
      "content":item.content,
      "metadata":{
        "topic":item.metadata.topic,
        "category":item.metadata.category,
        "agency":item.metadata.agency,
        "source":item.metadata.source,
        "added_at":item.metadata.added_at
      }
    })
    setShowDeleteModal(true)
    setDeleteId(item.id)
  }
  const handleDeleteDocs = async () =>{
    if (!deleteId) return
    try{
      const id = deleteId
      const res = await axios.delete(`http://localhost:8000/deletedocs/${id}`)
      setShowDeleteModal(false)
      fetchData()
      alert("delete success")
    }catch(error){
      console.log(error)
    }
  }
  const [data, setData] = useState([])
   useEffect(()=>{
    fetchData()
   }, [])

  return (
    <>
      <div className="flex min-h-screen bg-[#E7E9EB]">
        <AdminSidebar/>
        <main className="m-2 flex-1 overflow-y-auto">
          <p>filter</p>
          <table className="w-full border-collapse bg-white text-center text-sm font-light text-gray-500 table-fixed">
            <thead className="bg-[#007A6D]">
              <tr className="text-white">
                <th className="w-[100px] px-3 py-3 border-r">เนื้อหา</th>
                <th className="w-[100px] px-3 py-3 border-r">หัวข้อ</th>
                <th className="w-[100px] px-3 py-3 border-r">ประเภทของเนื้อหา</th>
                <th className="w-[80px] px-3 py-3 border-r">หน่วยงานที่เกี่ยวข้อง</th>
                <th className="w-[50px] px-3 py-3 border-r">แหล่งที่มา</th>
                <th className="w-[50px] px-3 py-3 border-r">วันเวลาที่เพิ่ม</th>
                <td className="bg-[#E7E9EB] w-[50px] px-3 py-3 truncate"></td>
              </tr>
            </thead>
            <tbody>
              {data.map((item)=>(
                <tr key={item.id} onClick={()=> handleViewModalopen(item)} className="hover:bg-gray-300 hover:text-white cursor-pointer">
                  <td className="w-[100px] px-3 py-3 truncate">{item.content}</td>
                  <td className="w-[100px] px-3 py-3 truncate">{item.metadata.topic}</td>
                  <td className="w-[100px] px-3 py-3 truncate">{item.metadata.category}</td>
                  <td className="w-[80px] px-3 py-3 truncate">{item.metadata.agency}</td>
                  <td className="w-[50px] px-3 py-3 truncate">{item.metadata.source}</td>
                  <td className="w-[50px] px-3 py-3 truncate">{item.metadata.added_at}</td>
                  {/*() => handleDeleteDocs(item.id) */}
                  <td className="w-[110px] px-2 py-3 cursor-pointer text-red-500 transition-all duration-200 hover:bg-red-500 hover:text-white" 
                    onClick={(e) => {e.stopPropagation(); handleDeleteModalopen(item);}}>
                      <div className="flex items-center justify-center gap-1">
                        <RiDeleteBin6Fill size={20} /> {/* ปรับขนาดไอคอนตรงนี้ */}
                        <span className="text-sm">ลบข้อมูล</span>
                      </div>
                   </td>
                </tr>
              ))}
            </tbody>
          </table>
        </main>
        <ViewDataModal isOpen={showDeleteModal} onClose={() => setShowDeleteModal(false)}>
          <h2 className="text-xl font-bold mb-2">ยืนยันการทำรายการ?</h2>
          <p className="text-gray-600 mb-6">
            คุณต้องการลบข้อมูลนี้ใช่หรือไม่? การกระทำนี้ไม่สามารถย้อนกลับได้
          </p>
          <div className="flex flex-col">
            <p>เนื้อหา:</p>
            <p className="text-gray-600 mb-6">{contentToDelete.content}</p>
            <p>หัวข้อ:</p>
            <p className="text-gray-600 mb-6">{contentToDelete.metadata.topic}</p>
            <p>ประเภทของเนื้อหา:</p>
            <p className="text-gray-600 mb-6">{contentToDelete.metadata.category}</p>
            <p>หน่วยงานที่เกี่ยวข้อง:</p>
            <p className="text-gray-600 mb-6">{contentToDelete.metadata.agency}</p>
            <p>แหล่งที่มา:</p>
            <p className="text-gray-600 mb-6">{contentToDelete.metadata.source}</p>
            <p>วันเวลาที่เพิ่ม:</p>
            <p className="text-gray-600 mb-6">{contentToDelete.metadata.added_at}</p>
            </div>
          <div className="flex justify-end gap-2">
            <button className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 cursor-pointer"onClick={() => setShowDeleteModal(false)}>
              ยกเลิก</button>
            <button className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 cursor-pointer"onClick={handleDeleteDocs}>
              ยืนยัน
            </button>
          </div>
        </ViewDataModal>
        <ViewDataModal isOpen={showVieweModal} onClose={() => setShowViewModal(false)}>
          <h2 className="text-xl font-bold mb-2">รายระเอียดของเอกสาร</h2>
          <div className="flex flex-col">
            <p>เนื้อหา:</p>
            <p className="text-gray-600 mb-6">{contentToView.content}</p>
            <p>หัวข้อ:</p>
            <p className="text-gray-600 mb-6">{contentToView.metadata.topic}</p>
            <p>ประเภทของเนื้อหา:</p>
            <p className="text-gray-600 mb-6">{contentToView.metadata.category}</p>
            <p>หน่วยงานที่เกี่ยวข้อง:</p>
            <p className="text-gray-600 mb-6">{contentToView.metadata.agency}</p>
            <p>แหล่งที่มา:</p>
            <p className="text-gray-600 mb-6">{contentToView.metadata.source}</p>
            <p>วันเวลาที่เพิ่ม:</p>
            <p className="text-gray-600 mb-6">{contentToView.metadata.added_at}</p>
            </div>
          <div className="flex justify-end gap-2">
            <button className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 cursor-pointer"onClick={() => setShowViewModal(false)}>
              ปิด
            </button>
          </div>
        </ViewDataModal>
      </div>
    </>
  )
}

export default ViewDocsPage