import { useEffect, useState } from "react";
import AdminSidebar from "../component/AdminSidebar";
import HistoryTable from "../component/HistoryTable";
import axios from "axios";
import HistoryChatModal from "../component/HistoryChatModal";

function ChatHistoryPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [totalPages, setTotalPages] = useState(1);
  const [isOpen, setIsOpen] = useState(false);
  const [selectedRow, setSelectedRow] = useState(null);

  const [filters, setFilters] = useState({
    agency: "",
    platform: "",
    statusFallback: null,
    timeRange: "",
    sortDate: "new",
    page: 1,
  });

  const handleChangePage = (direction) => {
    setFilters((prev) => ({
      ...prev,
      page: direction === "next" ? prev.page + 1 : Math.max(1, prev.page - 1),
    }));
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        console.log(filters);
        const response = await axios.get(
          `http://localhost:8000/admin/conversation`,
          {
            params: {
              agency: filters.agency,
              platform: filters.platform,
              statusFallback: filters.statusFallback,
              timeRange: filters.timeRange,
              sortDate: filters.sortDate,
              page: filters.page,
            },
          },
        );
        setData(response.data.items);
        setTotalPages(response.data.total_pages);
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
  }, [filters]);

  const handleRowClick = (rowData) => {
    setSelectedRow(rowData);
    console.log(selectedRow);
    setIsOpen(true);
  };

  return (
    <div className="flex min-h-screen bg-[#E7E9EB]">
      <AdminSidebar />
      <main className="m-2 flex-1 overflow-y-auto">
        <div className="flex flex-col md:flex-row md:items-center md:justify-end gap-4 bg-white p-3 rounded-lg shadow-sm mb-3">
          <div className="flex items-center justify-end gap-2 border-b md:border-none pb-3 md:pb-0">
            <div className="flex items-center gap-2">
              <button
                onClick={() => handleChangePage("prev")}
                disabled={filters.page === 1 || loading}
                className={`px-3 py-1 rounded border ${
                  filters.page === 1
                    ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                    : "bg-white hover:bg-gray-100"
                }`}
              >
                {"<"}
              </button>
              <span className="text-sm font-medium min-w-[60px] text-center">
                หน้า {filters.page}
              </span>
              <button
                onClick={() => handleChangePage("next")}
                disabled={filters.page >= totalPages || loading}
                className={`px-3 py-1 rounded border ${
                  filters.page >= totalPages
                    ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                    : "bg-white hover:bg-gray-100"
                }`}
              >
                {">"}
              </button>
            </div>
          </div>

          {/* ส่วน Dropdowns: จะเรียงเต็มจอในมือถือ และเรียงต่อกันในจอใหญ่ */}
          <div className="grid grid-cols-2 sm:grid-cols-3 md:flex md:flex-wrap items-center justify-end gap-2 flex-1">
            {/* หมวด */}
            <select
              value={filters.agency}
              onChange={(e) =>
                setFilters({ ...filters, agency: e.target.value, page: 1 })
              }
              className="text-xs sm:text-sm border border-gray-300 rounded p-2 bg-white w-full md:w-auto"
            >
              <option value="">หมวดทั้งหมด</option>
              <option value="กองบริหารวิชาการ">กองบริหารวิชาการ</option>
              <option value="สำนักดิจิทัลเทคโนโลยี">
                สำนักดิจิทัลเทคโนโลยี
              </option>
              <option value="กองกิจการนักศึกษา">กองกิจการนักศึกษา</option>
              <option value="อื่นๆ">อื่นๆ</option>
            </select>

            {/* platform */}
            <select
              value={filters.platform}
              onChange={(e) =>
                setFilters({ ...filters, platform: e.target.value, page: 1 })
              }
              className="text-xs sm:text-sm border border-gray-300 rounded p-2 bg-white w-full md:w-auto"
            >
              <option value="">Platform ทั้งหมด</option>
              <option value="LINE">LINE</option>
              <option value="Website">Website</option>
            </select>

            {/* is_fallback */}
            <select
              onChange={(e) =>
                setFilters({
                  ...filters,
                  statusFallback: e.target.value,
                  page: 1,
                })
              }
              className="text-xs sm:text-sm border border-gray-300 rounded p-2 bg-white w-full md:w-auto"
            >
              <option value="">สถานะทั้งหมด</option>
              <option value="false">ตอบได้ปกติ</option>
              <option value="true">ตอบไม่ได้ (Fallback)</option>
            </select>

            {/* timeRange */}
            <select
              value={filters.timeRange}
              onChange={(e) =>
                setFilters({ ...filters, timeRange: e.target.value, page: 1 })
              }
              className="text-xs sm:text-sm border border-gray-300 rounded p-2 bg-white w-full md:w-auto"
            >
              <option value="7">7 วันล่าสุด</option>
              <option value="1">24 ชั่วโมงล่าสุด</option>
              <option value="30">30 วันล่าสุด</option>
            </select>

            {/* เรียงจาก */}
            <select
              value={filters.sortDate}
              onChange={(e) =>
                setFilters({ ...filters, sortDate: e.target.value, page: 1 })
              }
              className="text-xs sm:text-sm border border-gray-300 rounded p-2 bg-white w-full md:w-auto"
            >
              <option value="new">ใหม่ไปเก่า</option>
              <option value="old">เก่าไปใหม่</option>
            </select>
          </div>
        </div>

        {/* ตารางข้อมูล */}
        <div className="bg-white rounded-lg shadow overflow-x-auto">
          {loading ? (
            <div className="p-10 text-center text-gray-500">
              กำลังโหลดข้อมูล...
            </div>
          ) : (
            <HistoryTable data={data} handleRowClick={handleRowClick} />
          )}
        </div>
        <div>
          {isOpen && selectedRow && (
            <HistoryChatModal
              data={selectedRow}
              isOpen={isOpen}
              onClose={() => setIsOpen(false)}
            />
          )}
        </div>
      </main>
    </div>
  );
}
export default ChatHistoryPage;
