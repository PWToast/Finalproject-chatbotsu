
import OverviewStatCard from '../component/OverviewStatCard';

function OverviewBoard({data}) {
  
    //fontColor ใส่ codeสีไม่ได้ ใช้text-teal-700แก้ขัดไปก่อน
    const total_users = (data?.web_users_count || 0)+(data?.line_users_count || 0);
    const statData = [
    { 
      id: 1,
      title: 'จำนวนผู้ใช้สะสม (คน)', 
      value: total_users.toLocaleString() ?? -1, 
      fontColor: 'text-black' 
    },
    { 
      id: 2,
      title: 'จำนวนบทสนทนาสะสม (ครั้ง)', 
      value: data?.total_conversation?.toLocaleString() ?? -1, 
      fontColor: 'text-black' 
    },
    { 
      id: 3,
      title: 'จำนวนคำถามที่ตอบได้ (คำถาม)', 
      value: -1, 
      fontColor: 'text-teal-700' 
    },
    { 
      id: 4,
      title: 'จำนวนคำถามนอกขอบเขต (คำถาม)', 
      value: -1, 
      fontColor: 'text-orange-400' 
    },
  ];
    return (
    <div className=''>
        <p className="m-1 text-3xl font-light-bold">ภาพรวม</p>
            <div className="grid lg:grid-cols-4 gap-2">
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