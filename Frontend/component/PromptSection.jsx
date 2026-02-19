import React from "react";

function PromptSection({ type, title, value, onChange, placeholder }) {
  return (
    /* ใช้ flex-1 เพื่อให้ทุก section กินพื้นที่เท่ากัน */
    <div className="p-4 flex flex-col flex-1 min-h-0">
      <div className="flex items-center gap-2 mb-2 shrink-0">
        <div className="px-2 py-1 rounded text-[13px] font-black uppercase text-teal-600">
          {type}
        </div>
        <h3 className="text-sm font-bold text-gray-700">{title}</h3>
      </div>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="bg-gray-200 w-full flex-1 p-4 rounded-xl resize-none text-sm leading-relaxed"
        placeholder={placeholder}
      />
    </div>
  );
}

export default PromptSection;
