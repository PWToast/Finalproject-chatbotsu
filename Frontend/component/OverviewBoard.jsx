
import OverviewStatCard from '../component/OverviewStatCard';

function OverviewBoard({data}) {
  
    //fontColor ใส่ codeสีไม่ได้ ใช้text-teal-700แก้ขัดไปก่อน
    const statData = [
    { 
      id: 1,
      title: 'จำนวนผู้ใช้สะสม (คน)', 
      value: 0,
      fontColor: 'text-black' 
    },
    { 
      id: 2,
      title: 'จำนวนบทสนทนาสะสม (ครั้ง)', 
      value: (data?.total_chat_web || 0) + (data?.total_chat_line || 0), 
      fontColor: 'text-black' 
    },
    { 
      id: 3,
      title: 'จำนวนคำถามที่ตอบได้ (คำถาม)', 
      value: data?.total_success || 0, 
      fontColor: 'text-teal-700' 
    },
    { 
      id: 4,
      title: 'จำนวนคำถามนอกขอบเขต (คำถาม)', 
      value:  data?.total_fallback || 0, 
      fontColor: 'text-orange-400' 
    },
  ];
    return (
    <div className=''>
            <div className="grid lg:grid-cols-4 gap-2 ">
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