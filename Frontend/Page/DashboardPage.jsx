import { useState,useEffect } from 'react'
import axios from 'axios'

import AdminSidebar from '../component/AdminSidebar';
import OverviewBoard from '../component/OverviewBoard';
import UserSourcePieChart from '../component/UserSourcePieChart';
import QuestionCategoryBarChart from '../component/QuestionCategoryBarChart';
import UserTrendLineChart from '../component/UserTrendLineChart';

function DashboardPage() {
  const [overviewData, setOverviewData] = useState(null);
  
    useEffect(() => {
      axios.get('http://localhost:8000/admin/overview').then(res => {
      setOverviewData(res.data);
    });
    }, []);
  return (
    <div className="flex h-screen bg-[#E7E9EB]">
      <AdminSidebar />
      <div className="m-2 flex-1 overflow-y-auto">
        <OverviewBoard data={overviewData}/>
        <div className="grid lg:grid-cols-2 gap-2">
          <div className='mt-2'>
            <UserSourcePieChart data={overviewData}/>
          </div>
          <div className='mt-2'>
            <QuestionCategoryBarChart/>
          </div>
        </div>
        <div className="grid lg:grid-cols-1">
          <div className='mt-2'>
            <UserTrendLineChart />
          </div>
        </div>
      </div>
    </div>
  );
}
export default DashboardPage