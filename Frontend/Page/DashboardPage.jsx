import AdminSidebar from '../component/AdminSidebar';
import OverviewBoard from '../component/OverviewBoard';
import UserSourcePieChart from '../component/UserSourcePieChart';

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
          {/* <div className='mt-2 border'> */}
            {/* <UserSourcePieChart /> */}
            
          {/* </div> */}
        </div>
      </div>
    </div>
  );
}
export default DashboardPage