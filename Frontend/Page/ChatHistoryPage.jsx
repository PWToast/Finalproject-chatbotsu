import { useEffect, useState } from "react";
import AdminSidebar from "../component/AdminSidebar";
import HistoryTable from "../component/HistoryTable";
import axios from "axios";

function ChatHistoryPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState("อื่นๆ");
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await axios.get(
          `http://localhost:8000/admin/conversation?filter=${filter}`,
        );
        setData(response.data.items);
      } catch (err) {
        setError("ไม่สามารถดึงข้อมูลได้ กรุณาลองใหม่");
        console.error("API Error:", err);
      } finally {
        setLoading(false);
      }
      console.log(loading);
      console.log(error);
    };

    fetchData();
  }, [filter]);
  return (
    <div className="flex min-h-screen bg-[#E7E9EB]">
      <AdminSidebar />
      <main className="m-2 flex-1 overflow-y-auto">
        <div className="flex">
          <div className="ml-auto py-2 flex items-center gap-2">
            <div>{"<"}</div>
            <div>{">"}</div>
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="text-sm border-1 border-gray-500 rounded p-1"
            >
              <option value="กองบริหารวิชาการ">กองบริหารวิชาการ</option>
              <option value="สำนักดิจิทัลเทคโนโลยี">
                สำนักดิจิทัลเทคโนโลยี
              </option>
              <option value="กองกิจการนักศึกษา">กองกิจการนักศึกษา</option>
              <option value="อื่นๆ">อื่นๆ</option>
              {/* <option value="อื่นๆ">ปีนี้</option> */}
            </select>
          </div>
        </div>
        {loading ? <p>กำลังโหลด...</p> : <HistoryTable data={data} />}
      </main>
    </div>
  );
}
export default ChatHistoryPage;
