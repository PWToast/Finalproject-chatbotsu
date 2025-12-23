import AdminSidebar from '../component/AdminSidebar';
import OverviewBoard from '../component/OverviewBoard';
import UserSourcePieChart from '../component/UserSourcePieChart';
import QuestionCategoryBarChart from '../component/QuestionCategoryBarChart';
import UserTrendLineChart from '../component/UserTrendLineChart';

function DashboardPage() {
  return (
    <div className="flex h-screen bg-[#E7E9EB]">
      <AdminSidebar/>
      <div className="m-2 flex-1 overflow-y-auto">
        <OverviewBoard/>
        <div className="grid lg:grid-cols-2 gap-2">
          <div className='mt-2'>
            <UserSourcePieChart />
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