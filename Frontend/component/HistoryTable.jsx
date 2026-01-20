import React from "react";

function HistoryTable({ data }) {
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
  //     },
  //     {
  //       id: 2,
  //       timestamp: "12-01-2026",
  //       userMessage: "yahoo",
  //       aiMessage: "hey",
  //       questionAgency: "อื่นๆ",
  //       platform: "WEB",
  //       statusFallback: false,
  //     },
  //     {
  //       id: 3,
  //       timestamp: "12-01-2026",
  //       userMessage: "asfdfaf",
  //       aiMessage: "unknown",
  //       questionAgency: "อื่นๆ",
  //       platform: "LINE",
  //       statusFallback: true,
  //     },
  //     {
  //       id: 1,
  //       timestamp: "12-01-2026",
  //       userMessage: "hello",
  //       aiMessage: "wassup",
  //       questionAgency: "อื่นๆ",
  //       platform: "LINE",
  //       statusFallback: false,
  //     },
  //     {
  //       id: 2,
  //       timestamp: "12-01-2026",
  //       userMessage: "yahoo",
  //       aiMessage: "hey",
  //       questionAgency: "อื่นๆ",
  //       platform: "WEB",
  //       statusFallback: false,
  //     },
  //     {
  //       id: 3,
  //       timestamp: "12-01-2026",
  //       userMessage: "asfdfaf",
  //       aiMessage: "unknown",
  //       questionAgency: "อื่นๆ",
  //       platform: "LINE",
  //       statusFallback: true,
  //     },
  //     {
  //       id: 1,
  //       timestamp: "12-01-2026",
  //       userMessage: "hello",
  //       aiMessage: "wassup",
  //       questionAgency: "อื่นๆ",
  //       platform: "LINE",
  //       statusFallback: false,
  //     },
  //     {
  //       id: 2,
  //       timestamp: "12-01-2026",
  //       userMessage: "yahoo",
  //       aiMessage: "hey",
  //       questionAgency: "อื่นๆ",
  //       platform: "WEB",
  //       statusFallback: false,
  //     },
  //     {
  //       id: 3,
  //       timestamp: "12-01-2026",
  //       userMessage: "asfdfaf",
  //       aiMessage: "unknown",
  //       questionAgency: "อื่นๆ",
  //       platform: "LINE",
  //       statusFallback: true,
  //     },
  //     {
  //       id: 1,
  //       timestamp: "12-01-2026",
  //       userMessage: "hello",
  //       aiMessage: "wassup",
  //       questionAgency: "อื่นๆ",
  //       platform: "LINE",
  //       statusFallback: false,
  //     },
  //   ];
  return (
    <div className="overflow-hidden rounded-lg border border-gray-200 shadow-md">
      <div className="overflow-x-auto">
        <table className="w-full border-collapse bg-white text-left text-sm text-gray-500">
          <thead className="bg-[#007A6D]">
            <tr className="text-white">
              <th className="px-3 py-3 border-r-1">Timestamp</th>
              <th className="px-3 py-3 border-r-1">User Message</th>
              <th className="px-3 py-3 border-r-1">AI Message</th>
              <th className="px-3 py-3 border-r-1">Question Agency</th>
              <th className="px-3 py-3 border-r-1">Platform</th>
              <th className="px-3 py-3 border-r-1">Status (Fallback)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 border-t border-gray-100">
            {data.map((user, index) => (
              <tr
                key={index}
                className={`transition-colors ${
                  user.is_fallback
                    ? "bg-yellow-50 hover:bg-yellow-100"
                    : "bg-white hover:bg-gray-50"
                }`}
              >
                <td className="px-6 py-4">{user.timestamp}</td>
                <td className="px-6 py-4">
                  {/* <span className="inline-flex items-center gap-1 rounded-full bg-blue-50 px-2 py-1 text-xs font-semibold text-blue-600">
                  {user.role}
                </span> */}
                  {user.user_message}
                </td>
                <td className="px-6 py-4">{user.ai_message}</td>
                <td className="px-6 py-4">{user.question_agency}</td>
                <td className="px-6 py-4">{user.platform}</td>
                <td className="px-6 py-4">
                  {user.is_fallback ? (
                    <span className="text-black-500">true</span>
                  ) : (
                    <span className="text-black-500">false</span>
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
