import React, { useState, useEffect } from "react";
import axios from "axios";
import AdminSidebar from "../component/AdminSidebar";
import PromptSection from "../component/PromptSection";
import ConfirmPromptModal from "../component/ConfirmPromptModal";
import { useAuth } from "../service/Auth";
// กำหนด URL ของ API (ปรับตามจริง)

function EditPromptPage() {
  useAuth("admin"); //auth
  const [selectedNode, setSelectedNode] = useState("decision");
  const [systemContent, setSystemContent] = useState("");
  const [humanContent, setHumanContent] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token"); //auth
    const fetchPromptData = async () => {
      setLoading(true);
      try {
        //ดึง promptที่ใช้อยู่มาดู
        const response = await axios.get(
          `http://localhost:8000/admin/get-prompt/${selectedNode}`,
          {
            headers: {
              //auth
              Authorization: `Bearer ${token}`,
            },
          },
        );
        if (response.data && response.data.messages) {
          const messages = response.data.messages;
          const sys = messages.find((m) => m.role === "system")?.content || "";
          const hum = messages.find((m) => m.role === "human")?.content || "";
          setSystemContent(sys);
          setHumanContent(hum);
        }
      } catch (error) {
        console.error("Error fetching prompt:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchPromptData();
  }, [selectedNode]);

  const openModal = (type) => {
    setModalType(type);
    setShowModal(true);
  };

  const handleConfirm = async () => {
    const token = localStorage.getItem("token"); // ดึง token เตรียมไว้
    try {
      if (modalType === "save") {
        const payload = {
          node_id: selectedNode,
          messages: [
            { role: "system", content: systemContent },
            { role: "human", content: humanContent },
          ],
        };
        //อัปเดต prompt
        await axios.post(`http://localhost:8000/admin/update-prompt`, payload, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log("บันทึกสำเร็จ");
      } else {
        // คืนค่าเริ่มต้น prompt
        const response = await axios.get(
          `http://localhost:8000/admin/reset-prompt/${selectedNode}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );
        setSystemContent(response.data.system);
        setHumanContent(response.data.human);
      }
    } catch (error) {
      console.error("ไม่สามารถแก้ไข prompt ได้:", error);
      if (error.response?.status === 401) {
        alert("เซสชันหมดอายุ กรุณาเข้าสู่ระบบใหม่");
      } else {
        alert("เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์");
      }
    } finally {
      setShowModal(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#E7E9EB] overflow-hidden">
      <AdminSidebar />
      <main className="m-2 flex-1 flex flex-col min-w-0">
        <div className="flex flex-col md:flex-row md:items-center md:justify-end gap-4 bg-white p-3 rounded-lg shadow-sm mb-3 shrink-0">
          <div className="flex items-center justify-end gap-2 w-full md:w-auto">
            <label className="text-sm font-medium text-gray-700 whitespace-nowrap">
              เลือกส่วนที่ต้องการแก้ไข prompt :
            </label>
            <select
              value={selectedNode}
              onChange={(e) => setSelectedNode(e.target.value)}
              className="text-xs sm:text-sm border border-gray-300 rounded-md p-2 bg-white w-full md:w-auto cursor-pointer outline-none focus:ring-2 focus:ring-teal-500"
            >
              <option value="decision">การตัดสินใจ (Decision)</option>
              <option value="rewrite">การเกลาคำถาม (Rewrite)</option>
              <option value="rag">การสืบค้นข้อมูล (RAG)</option>
              <option value="general">การสนทนาทั่วไป (General)</option>
            </select>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow flex-1 flex flex-col overflow-hidden min-h-0 relative">
          {/* แสดง Loading Overlay ขณะโหลดข้อมูล */}
          {loading && (
            <div className="absolute inset-0 bg-white/50 z-10 flex items-center justify-center">
              <div className="text-teal-600 font-bold">กำลังโหลดข้อมูล...</div>
            </div>
          )}

          <PromptSection
            type="system"
            title="คำสั่งควบคุมระบบ"
            value={systemContent}
            onChange={setSystemContent}
            placeholder="กำหนดพฤติกรรมหลัก..."
          />

          <div className="border-t border-gray-100"></div>

          <PromptSection
            type="human"
            title="รูปแบบคำถาม"
            value={humanContent}
            onChange={setHumanContent}
            placeholder="คำถามล่าสุด: {user_message}"
          />

          <div className="p-4 bg-gray-50 flex flex-col sm:flex-row justify-between items-center gap-3 shrink-0">
            <button
              onClick={() => openModal("reset")}
              className="text-sm font-medium text-gray-500 hover:text-red-600 transition-colors w-full sm:w-auto py-2"
            >
              คืนค่าเริ่มต้น
            </button>
            <button
              onClick={() => openModal("save")}
              className="bg-teal-600 hover:bg-teal-700 text-white font-bold py-3 px-10 rounded-lg shadow-md w-full sm:w-auto text-sm"
            >
              บันทึกการเปลี่ยนแปลง
            </button>
          </div>
        </div>
      </main>

      <ConfirmPromptModal
        isModalOpen={showModal}
        type={modalType}
        onClose={() => setShowModal(false)}
        onConfirm={handleConfirm}
      />
    </div>
  );
}

export default EditPromptPage;
