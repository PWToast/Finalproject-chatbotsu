function LogOutModal({ isModalOpen, onClose, onConfirm }) {
  if (!isModalOpen) return null;

  return (
    <div
      className="fixed inset-0 bg-black/50 z-50 flex justify-center items-center"
      onClick={onClose}
    >
      <div
        className="mx-4 bg-white p-8 rounded-2xl shadow-2xl w-full max-w-sm flex flex-col text-center"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="text-xl font-bold text-black-500 mb-8">
          คุณต้องการออกจากระบบหรือไม่?
        </div>
        <div className="flex flex-row gap-3 mt-6">
          <button
            className="flex-1 py-3 px-4 bg-gray-300 hover:bg-gray-400 text-gray-700 font-semibold rounded-xl transition-colors"
            onClick={onClose}
          >
            ยกเลิก
          </button>
          <button
            className="flex-1 py-3 px-4 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-xl transition-colors shadow-md shadow-red-100"
            onClick={onConfirm}
          >
            ออกจากระบบ
          </button>
        </div>
      </div>
    </div>
  );
}
export default LogOutModal;
