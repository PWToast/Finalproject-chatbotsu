import { 
  ComputerDesktopIcon, 
  DocumentTextIcon, 
  ChatBubbleLeftRightIcon 
} from '@heroicons/react/24/outline';
import { Link } from 'react-router-dom';

function AdminSidebar() {
  // เพิ่มปุ่ม navตรงนี้
  const navItems = [
    { 
      name: 'Dashboard', 
      icon: ComputerDesktopIcon,
      path: '/dashboard',
    },
    { 
      name: 'Manage RAG Sources', 
      icon: DocumentTextIcon,
      path: '/manage-rag-soures',  
    },
    { 
      name: 'Conversation History', 
      icon: ChatBubbleLeftRightIcon,
      path: '/conversation-history', 
    },
  ];

  return (
    <div className="flex flex-col w-64 h-screen bg-teal-700 text-white">
      <div className="px-9 py-6 text-3xl font-light-bold border-b border-teal-600">
        Admin Panel
      </div>
      <nav className="flex-1 px-4 py-4 space-y-3">
        {navItems.map((item) => {
          const Icon = item.icon; 
          return (
            // ต้องเปลี่ยน a เป็น Link ตอนกดจะได้เปลี่ยนหน้า
            <a
              key={item.name}
              href={item.path} //ต้องเปลี่ยนเป็น to={item.path}
              className="
                flex items-center p-3 rounded-lg 
                text-xl font-light leading-snug 
                hover:bg-teal-600 transition duration-150"
            >
              <Icon className="w-6 h-6 mr-3" />
              {item.name}
            </a>
          );
        })}
      </nav>
    </div>
  );
};

export default AdminSidebar;