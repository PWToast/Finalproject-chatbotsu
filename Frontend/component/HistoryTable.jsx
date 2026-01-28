import React from "react";

function HistoryTable({ data, handleRowClick }) {
  //ใส่ prop { data }
  //   const data = [
  //     {
  //       id: 1,
  //       timestamp: "12-01-2026",
  //       userMessage: "hello",
  //       aiMessage: "wassup",
  //       questionAgency: "อื่นๆ",
  //       platform: "LINE",
  //       statusFallback: false,
  //     }
  //   ];

  const formatThaiDate = (raw) =>
    raw
      ? new Date(raw).toLocaleString("sv-SE", { timeZone: "Asia/Bangkok" })
      : "-";
  return (
    <div className="overflow-hidden rounded-lg border border-gray-200 shadow-md">
      <div className="overflow-x-auto">
        <table className="w-full border-collapse bg-white text-center text-sm font-light text-gray-500 table-fixed">
          <thead className="bg-[#007A6D]">
            <tr className="text-white">
              <th className="w-[100px] px-3 py-3 border-r-1">วัน-เวลา</th>
              <th className="w-[150px] px-3 py-3 border-r-1">คำถามจากผู้ใช้</th>
              <th className="w-[150px] px-3 py-3 border-r-1">คำตอบจาก AI</th>
              <th className="w-[80px] px-3 py-3 border-r-1">
                หมวดที่เกี่ยวข้อง
              </th>
              <th className="w-[50px] px-3 py-3 border-r-1">ช่องทาง</th>
              <th className="w-[50px] px-3 py-3 border-r-1">สถานะการตอบกลับ</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 border-t border-gray-100">
            {data.map((user, index) => (
              <tr
                key={index}
                onClick={() => handleRowClick(user)}
                className={`transition-colors ${
                  user.is_fallback
                    ? "bg-yellow-50 hover:bg-yellow-100"
                    : "bg-white hover:bg-gray-50"
                }`}
              >
                <td className="px-6 py-4">{formatThaiDate(user.timestamp)}</td>
                <td className="px-3 py-4">
                  <div className="truncate w-full" title={user.user_message}>
                    {user.user_message}
                  </div>
                </td>
                <td className="px-3 py-4">
                  <div className="truncate w-full" title={user.ai_message}>
                    {user.ai_message}
                  </div>
                </td>
                <td className="px-6 py-4">{user.question_agency}</td>
                <td className="px-6 py-4">{user.platform}</td>
                <td className="px-6 py-4">
                  {user.is_fallback ? (
                    <span className="text-black-500">ตอบไม่ได้</span>
                  ) : (
                    <span className="text-black-500">ตอบได้</span>
                  )}
                </td>
                {/* <td className="px-6 py-4">
                <button className="text-blue-600 hover:underline">แก้ไข</button>
              </td> */}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default HistoryTable;
