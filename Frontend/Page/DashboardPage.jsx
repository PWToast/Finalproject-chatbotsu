import { useState,useEffect } from 'react'
import axios from 'axios'

import AdminSidebar from '../component/AdminSidebar';
import OverviewBoard from '../component/OverviewBoard';
import UserSourcePieChart from '../component/UserSourcePieChart';
import QuestionCategoryBarChart from '../component/QuestionCategoryBarChart';
import UserTrendLineChart from '../component/UserTrendLineChart';

function DashboardPage() {
  const [summaryData, setSummaryData] = useState(null);
  useEffect(() => {
    axios.get('http://localhost:8000/admin/summary')
        .then(res => setSummaryData(res.data))
        .catch(err => console.error("Error fetching summary:", err));
    console.log(summaryData?.total_chat_web)    
}, []);
  
  return (
    <div className="flex h-screen bg-[#E7E9EB]">
      <AdminSidebar />
      <div className="m-2 flex-1 overflow-y-auto">
        <OverviewBoard data={summaryData}/>
        <div className="grid lg:grid-cols-2 gap-2">
          <div className='mt-2'>
            <UserSourcePieChart data={summaryData}/>
          </div>
          <div className='mt-2'>
            <QuestionCategoryBarChart data={summaryData}/>
          </div>
        </div>
        <div className="grid lg:grid-cols-1">
          <div className='mt-2'>
            <UserTrendLineChart data={summaryData}/>
          </div>
        </div>
      </div>
    </div>
  );
}
export default DashboardPage