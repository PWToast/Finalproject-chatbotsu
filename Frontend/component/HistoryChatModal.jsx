function HistoryChatModal({ data, isOpen, onClose }) {
  if (!isOpen) return null;
  const formatThaiDate = (raw) =>
    raw
      ? new Date(raw).toLocaleString("sv-SE", { timeZone: "Asia/Bangkok" })
      : "-";
  return (
    // พื้นหลัง
    <div
      className="fixed inset-0 bg-black/50 z-50 flex justify-center items-center"
      onClick={onClose}
    >
      {/* modal */}
      <div
        className="mx-4 bg-white p-6 rounded-lg shadow-lg w-full max-w-lg max-h-[90vh] flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="text-xl font-bold mb-4 flex-none">
          รายละเอียดการสนทนา
        </div>
        <div className="overflow-y-auto pr-2 custom-scrollbar">
          <p className="font-semibold text-gray-700">คำถามจากผู้ใช้:</p>
          <p className="mb-2 text-gray-600 break-words">{data.user_message}</p>
          <p className="font-semibold text-gray-700">คำถามที่ rewrite แล้ว:</p>
          {/* เก็บข้อมูล rewriteด้วย */}
          <p className="mb-2 text-gray-600 break-words">
            {data.rewritten_question}
          </p>
          <p className="font-semibold text-gray-700">คำตอบจาก AI:</p>
          <p className="mb-2 text-gray-600 break-words">{data.ai_message}</p>
          <p className="font-semibold text-gray-700">สถานะการตอบกลับ:</p>
          <p
            className={`mb-2 break-words ${data.is_fallback === true ? "text-red-500" : "text-green-600"}`}
          >
            {data.is_fallback === true ? "ตอบไม่ได้ (fallback)" : "ตอบได้"}
          </p>
          <p className="font-semibold text-gray-700">หมวดที่เกี่ยวข้อง:</p>
          <p className="mb-2 text-gray-600 break-words">
            {data.question_agency}
          </p>
          <p className="font-semibold text-gray-700">ช่องทาง:</p>
          <p className="mb-2 text-gray-600 break-words">{data.platform}</p>
          <p className="font-semibold text-gray-700">วัน-เวลา:</p>
          <p className="mb-2 text-gray-600 break-words">
            {formatThaiDate(data.timestamp)}
          </p>
        </div>
        <div className="flex justify-end mt-4 pt-2 border-t flex-none">
          <button
            className="mt-4 px-4 py-2 bg-gray-500 text-white hover:bg-gray-600 rounded"
            onClick={onClose}
          >
            ปิด
          </button>
        </div>
      </div>
    </div>
  );
}

export default HistoryChatModal;
