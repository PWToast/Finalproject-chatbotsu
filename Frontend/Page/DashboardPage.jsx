import AdminSidebar from '../component/AdminSidebar';
import OverviewBoard from '../component/OverviewBoard';

function DashboardPage({children}) {
  return (
    <div className="flex h-screen bg-[#E7E9EB]">
      <AdminSidebar/>
      <div className="flex-1 overflow-y-auto">
        <OverviewBoard/>
        <main className="p-4">
          {children}
        </main>
      </div>
    </div>
  );
}
export default DashboardPage