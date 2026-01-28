const ViewDataModal = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return (
    // 1. Overlay: พื้นหลังทึบ เต็มหน้าจอ
    <div 
      className="fixed inset-0 bg-black/50 flex justify-center items-center z-50"
      onClick={onClose}
    >
      {/* 2. Content: กล่องเนื้อหาตรงกลาง */}
      <div 
        className="bg-white p-6 rounded-lg shadow-lg w-11/12 max-w-[90vh] relative max-h-[90vh] overflow-y-auto custom-scrollbar"
        onClick={(e) => e.stopPropagation()}
      >
        {/* ปุ่มกากบาทมุมขวาบน */}
        <button 
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-700 font-bold cursor-pointer"
          onClick={onClose}
        >
          X
        </button>
        
        {/* เนื้อหาที่จะใส่เข้ามา */}
        {children}
      </div>
    </div>
  );
};

export default ViewDataModal;