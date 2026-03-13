import { useState } from "react";
import {
  ComputerDesktopIcon,
  DocumentTextIcon,
  ChatBubbleLeftRightIcon,
  PowerIcon,
  Bars3Icon,
  XMarkIcon,
  PencilSquareIcon,
} from "@heroicons/react/24/outline";
import { Link, useNavigate } from "react-router-dom";
import LogOutModal from "./LogOutModal";
function AdminSidebar() {
  const [isOpen, setIsOpen] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();

  const navItems = [
    { name: "แดชบอร์ด", icon: ComputerDesktopIcon, path: "/dashboard" },
    {
      name: "เพิ่มข้อมูล RAG",
      icon: DocumentTextIcon,
      path: "/manage-rag-soures",
    },
    {
      name: "จัดการข้อมูล RAG",
      icon: DocumentTextIcon,
      path: "/view-docs-page",
    },
    {
      name: "ประวัติการสนทนา",
      icon: ChatBubbleLeftRightIcon,
      path: "/conversation-history",
    },
    {
      name: "แก้ไข prompt",
      icon: PencilSquareIcon,
      path: "/edit-prompt",
    },
    { name: "ออกจากระบบ", icon: PowerIcon, path: true },
  ];
  const handleLogoutConfirm = () => {
    localStorage.removeItem("token");
    console.log("ออกจากระบบแล้ว!");
    setIsModalOpen(false);
    navigate("/");
  };
  return (
    <>
      <button
        className="lg:hidden fixed top-4 left-4 border-1 z-50 p-2 bg-[#007A6D] text-white rounded-md"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? (
          <XMarkIcon className="w-6 h-6" />
        ) : (
          <Bars3Icon className="w-6 h-6" />
        )}
      </button>

      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setIsOpen(false)}
        ></div>
      )}

      <div
        className={`
        fixed inset-y-0 left-0 z-40 w-64 bg-[#007A6D] text-white transform transition-transform duration-300 ease-in-out
        lg:translate-x-0 lg:static lg:inset-0
        ${isOpen ? "translate-x-0" : "-translate-x-full"}
      `}
      >
        <div className="py-4 text-center text-2xl font-bold border-b border-teal-600">
          แผงควบคุม
        </div>
        <nav className="flex-1 px-4 py-4 space-y-3">
          {navItems.map((item) => {
            const Icon = item.icon;
            if (item.name === "ออกจากระบบ") {
              return (
                <button
                  key={item.name}
                  onClick={() => {
                    // setIsOpen(false); // ปิด Sidebar มือถือ
                    setIsModalOpen(true);
                  }}
                  className="w-full flex items-center p-3 rounded-lg text-lg font-light hover:bg-teal-600 transition"
                >
                  <Icon className="w-6 h-6 mr-3" />
                  {item.name}
                </button>
              );
            }
            return (
              <Link
                key={item.name}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className="flex items-center p-3 rounded-lg text-lg font-light hover:bg-teal-600 transition"
              >
                <Icon className="w-6 h-6 mr-3" />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>
      <LogOutModal
        isModalOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onConfirm={handleLogoutConfirm}
      />
    </>
  );
}

export default AdminSidebar;
