function ConfirmPromptModal({ isModalOpen, onClose, onConfirm, type }) {
  if (!isModalOpen) return null;

  // modal ของ ยืนยัน กับ ค่าเริ่มต้น
  const isSave = type === "save";
  const title = isSave ? "ยืนยันการบันทึก Prompt?" : "คืนค่าเริ่มต้น?";
  const confirmText = isSave ? "บันทึก" : "คืนค่าเริ่มต้น";
  const confirmColor = isSave
    ? "bg-teal-600 hover:bg-teal-700 shadow-teal-100"
    : "bg-gray-800 hover:bg-black shadow-gray-200";

  return (
    <div
      className="fixed inset-0 bg-black/50 z-50 flex justify-center items-center"
      onClick={onClose}
    >
      <div
        className="mx-4 bg-white p-8 rounded-2xl shadow-2xl w-full max-w-sm flex flex-col text-center"
        onClick={(e) => e.stopPropagation()}
      >
        {/* หัวข้อ */}
        <div className="text-xl font-bold text-gray-800 mb-4">{title}</div>

        {/* ข้อความ */}
        <div className="text-sm text-gray-500 mb-6">
          {isSave
            ? "การเปลี่ยนแปลงนี้จะมีผลต่อการตอบกลับของแชทบอทในทันที"
            : "ระบบจะกลับไปใช้ prompt เริ่มต้นของระบบ มีผลเฉพาะส่วนนี้เท่านั้น"}
        </div>

        {/* ปุ่มกดยืนยัน ยกเลิก */}
        <div className="flex flex-row gap-3 mt-4">
          <button
            className="flex-1 py-3 px-4 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold rounded-xl transition-colors"
            onClick={onClose}
          >
            ยกเลิก
          </button>
          <button
            className={`flex-1 py-3 px-4 ${confirmColor} text-white font-semibold rounded-xl`}
            onClick={onConfirm}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmPromptModal;
