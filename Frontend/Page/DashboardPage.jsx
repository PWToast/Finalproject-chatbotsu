import { useState, useEffect } from "react";
import axios from "axios";

import AdminSidebar from "../component/AdminSidebar";
import OverviewBoard from "../component/OverviewBoard";
import UserSourcePieChart from "../component/UserSourcePieChart";
import QuestionCategoryBarChart from "../component/QuestionCategoryBarChart";
import UserTrendLineChart from "../component/UserTrendLineChart";
import { useAuth } from "../service/Auth";

function DashboardPage() {
  useAuth("admin"); //auth
  const [summaryData, setSummaryData] = useState(null);
  useEffect(() => {
    const token = localStorage.getItem("token"); //auth
    axios
      .get("http://localhost:8000/admin/summary", {
        headers: {
          //auth
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        console.log("Raw Data from API:", res.data);
        setSummaryData(res.data);
      })
      .catch((err) => console.error("Error fetching summary:", err));
  }, []);
  return (
    <div className="flex min-h-screen bg-[#E7E9EB]">
      <AdminSidebar />
      <main className="m-2 flex-1 overflow-y-auto">
        <OverviewBoard data={summaryData} />
        <div className="grid lg:grid-cols-2 gap-2">
          <div className="mt-2">
            <UserSourcePieChart data={summaryData} />
          </div>
          <div className="mt-2">
            <QuestionCategoryBarChart data={summaryData} />
          </div>
        </div>
        <div className="grid lg:grid-cols-1">
          <div className="mt-2">
            <UserTrendLineChart data={summaryData} />
          </div>
        </div>
      </main>
    </div>
  );
}
export default DashboardPage;
