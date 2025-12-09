import AdminSidebar from '../component/AdminSidebar';

function DashboardPage({children}) {
  return (
    <div className="flex h-screen bg-[#E7E9EB]">
      <AdminSidebar/>
      <div className="flex-1 overflow-y-auto">
        {/* <Header /> */}
        <main className="p-4">
          {children}
        </main>
      </div>
    </div>
  );
}
export default DashboardPage