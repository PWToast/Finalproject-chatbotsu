import OverviewStatCard from '../component/OverviewStatCard';

function OverviewBoard() {
    // โหลดข้อมูลตรงนี้ 

    // fontColor ใส่ codeสีไม่ได้ ใช้text-teal-700แก้ขัด
    const statData = [
    { 
      id: 1,
      title: 'จำนวนผู้ใช้สะสม (คน)', 
      value: 5, 
      fontColor: 'text-black' 
    },
    { 
      id: 2,
      title: 'จำนวนบทสนทนา (ครั้ง)', 
      value: 5, 
      fontColor: 'text-black' 
    },
    { 
      id: 3,
      title: 'จำนวนคำถามที่ตอบได้ (คำถาม)', 
      value: 4, 
      fontColor: 'text-teal-700' 
    },
    { 
      id: 4,
      title: 'จำนวนคำถามนอกขอบเขต (คำถาม)', 
      value: 1, 
      fontColor: 'text-orange-400' 
    },
  ];
    return (
    <div className="p-2">
        <p className="px-1 text-3xl font-light-bold">Overview</p>
            <div className="my-1 grid lg:grid-cols-4 gap-6">
                {statData.map(data => (
                <OverviewStatCard 
                    key={data.id}
                    title={data.title}
                    value={data.value}
                    fontColor={data.fontColor}
                />))}
            </div>
    </div>
    );
};
export default OverviewBoard;